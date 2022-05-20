from nbformat import write
import pandas as pd
import numpy as np
import streamlit as st
import plotly as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from io import StringIO

# Uploader widget
st.set_page_config(layout="wide")
st.sidebar.title(
    'Welcome!')
st.sidebar.image("https://i.postimg.cc/qRw343dv/sar.jpg")
ca01, ca01a,ca01b= st.columns([2,6,2])
with ca01a:
    st.image("https://i.postimg.cc/qBKC1T8b/online-data.jpg")
c01, c01a,c01b= st.columns([1,6,1])
with c01a:
    st.title("**DataCo Global -- Business Performance Analysis**")

st.write('Dear reviewer from **DataCo Global**, welcome to your streamlit reporting application.')
st.write('In order to start reviewing your reports, please upload the desired data that you wish to analyze.') 
st.write('After uplaoding is complete, you can select from the list of sections that you want to review. You can use the filters provided on the left to filter your data via **Year** and via **Market**')

filename  = st.sidebar.file_uploader("Upload your CSV file:",type = ['csv'])
@st.cache(hash_funcs={StringIO: StringIO.getvalue},allow_output_mutation=True)
def try_read_df(file_uploaded):
    return (pd.read_csv(file_uploaded,encoding='unicode_escape'))


if filename :
    data = try_read_df(filename )
    

        ## Data Cleaning

    ## Creating full Name column

    data["Customer Name"] = data['Customer Fname'].astype(str) + " " + data['Customer Lname'].astype(str) 

    ## removing the unused columns

    data1 = data.drop(["Customer Email","Customer Password","Customer Fname", "Customer Lname","Customer Street","Customer Zipcode","Latitude","Longitude",
                    "Order Item Id","Order Zipcode","Product Card Id","Product Category Id","Product Description",
                    "Product Image","Product Status","Product Price","Order Item Discount Rate","Benefit per order",
                    "Sales per customer","Order Item Profit Ratio","Order Customer Id",'Sales'],axis=1) 

    ## renaming the columns

    data1 = data1.rename(columns = {'Type':'Transaction Type','Late_delivery_risk':'Late delivery risk', 
                                'Category Id':'Product Category Code','order date (DateOrders)':'Order Date',
                                'Order Item Cardprod Id':'Product Code','Order Item Product Price':'Item Price',
                                'Order Item Quantity':'Ordered Quantity','Order Item Total':'Total Item Sale', 
                                'Order Profit Per Order':'Total Item Profit','shipping date (DateOrders)':'Shipping Date'})

    ## converting orders and shipping columns to date format first 

    data1['Order Date']=pd.to_datetime(data1['Order Date'])
    data1['Shipping Date']=pd.to_datetime(data1['Shipping Date'])

    ## adding the year, quarter, month, and day columns

    data1['Year'] = pd.DatetimeIndex(data1['Order Date']).year
    data1['Month'] = pd.DatetimeIndex(data1['Order Date']).month
    data1['Day'] = pd.DatetimeIndex(data1['Order Date']).day
    data1['Quarter'] = data1['Order Date'].dt.quarter

    ## changing the type of the columns to categorical and assigning date format to the order and shipping date

    data1['Late delivery risk'] = data1['Late delivery risk'].map({1:'yes', 0: 'no'})
    #data1['Month'] = data1['Month'].map({1:'January', 2: 'February',3:'March',4:'April', 5:'May', 6:'June',
                                    #  7: 'July', 8:'August', 9: 'September', 10: ' October', 11: 'November', 12: 'December'})
    #data1['Month'] = data1['Month'].astype('category')
    data1['Transaction Type'] = data1['Transaction Type'].astype('category')
    data1['Delivery Status'] = data1['Delivery Status'].astype('category')
    data1['Category Name'] = data1['Category Name'].astype('category')
    data1['Customer City'] = data1['Customer City'].astype('category')
    data1['Customer Country'] = data1['Customer Country'].astype('category')
    data1['Customer Segment'] = data1['Customer Segment'].astype('category')
    data1['Customer State'] = data1['Customer State'].astype('category')
    data1['Department Name'] = data1['Department Name'].astype('category')
    data1['Market'] = data1['Market'].astype('category')
    data1['Order Country'] = data1['Order Country'].astype('category')
    data1['Order Region'] = data1['Order Region'].astype('category')
    data1['Order State'] = data1['Order State'].astype('category')
    data1['Order Status'] = data1['Order Status'].astype('category')
    data1['Order City'] = data1['Order City'].astype('category')
    data1['Product Name'] = data1['Product Name'].astype('category')
    data1['Shipping Mode'] = data1['Shipping Mode'].astype('category')
    data1['Customer Name'] = data1['Customer Name'].astype('category')
    data1['Late delivery risk'] = data1['Late delivery risk'].astype('category')
    data1['Product Category Code'] = data1['Product Category Code'].astype('category')
    data1['Customer Id'] = data1['Customer Id'].astype('category')
    data1['Department Id'] = data1['Department Id'].astype('category')
    data1['Order Id'] = data1['Order Id'].astype('category')
    data1['Product Code'] = data1['Product Code'].astype('category')
    data1['Quarter'] = data1['Quarter'].map({1:'Q1', 2: 'Q2',3: 'Q3',4: 'Q4'})
    data1['Quarter'] = data1['Quarter'].astype('category')

## drop any na left in the data

    data1=data1.dropna()

    ### Sales performance
    sales = data1

    positions = list(sales["Year"].drop_duplicates())
    position_choice = st.sidebar.multiselect(
        'Choose Reporting Year:', positions, default=positions)

    positions2 = list(sales["Market"].drop_duplicates())
    position_choice2 = st.sidebar.multiselect(
        'Choose Market:', positions2, default=positions2)   

    ## Total discount

    sales=data1

    sales5=sales.groupby(['Market','Year'])['Order Item Discount'].sum()
    sales5=sales5.to_frame().reset_index()

    sales5 = sales5[sales5['Year'].isin(position_choice)]
    sales5 = sales5[sales5['Market'].isin(position_choice2)]

    sales5a= sales5.groupby(['Year'])['Order Item Discount'].sum()
    sales5a= sales5a.to_frame().reset_index()

    #number of orders

    sales6 = sales[['Year','Market','Order Id']]
    sales6= sales6.drop_duplicates(subset='Order Id', keep='first').reset_index()

    sales6 = sales6[sales6['Year'].isin(position_choice)]
    sales6 = sales6[sales6['Market'].isin(position_choice2)]

    sales6a= len(sales6['Order Id'])
    sales6a

    ## number of distinct products

    sales8 = sales[['Year','Market','Product Name']]
    sales8= sales8.drop_duplicates(subset='Product Name', keep='first').reset_index()

    sales8 = sales8[sales8['Year'].isin(position_choice)]
    sales8 = sales8[sales8['Market'].isin(position_choice2)]

    sales8a= len(sales8['Product Name'])
    sales8a

    ## Total ordered quantities

    sales7=sales.groupby(['Market','Year'])['Ordered Quantity'].sum()
    sales7=sales7.to_frame().reset_index()

    sales7 = sales7[sales7['Year'].isin(position_choice)]
    sales7 = sales7[sales7['Market'].isin(position_choice2)]

    sales7a= sales7.groupby(['Year'])['Ordered Quantity'].sum()
    sales7a= sales7a.to_frame().reset_index()

    ## Total Sales per year


    sales=data1

    sales1=sales.groupby(['Market','Year'])['Total Item Sale'].sum()
    sales2=sales1.to_frame().reset_index()

    sales2 = sales2[sales2['Year'].isin(position_choice)]
    sales2 = sales2[sales2['Market'].isin(position_choice2)]

    sales2a= sales2.groupby(['Year'])['Total Item Sale'].sum()
    sales2a= sales2a.to_frame().reset_index()

    fig207 = go.Figure(go.Bar(
                    x= sales2a['Year'],
                    y= sales2a['Total Item Sale'],
                    marker_color='#3cabe2',
                    opacity=0.9,
                    orientation='v'))
    fig207.update_xaxes(type='category')
    fig207.update_layout(
            title_text='Sales Per Year', # title of plot
            titlefont =dict(
                family="Arial Black",
                size=16,
                color='#000000'
            ),font=dict(
                    family="Arial",
                    size=10,
                    color='#000000'
                ),
            xaxis_title_text='', # xaxis label
            yaxis_title_text='', # yaxis label
            bargap=0.2, # gap between bars of adjacent location coordinates
            bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates
        
    ## Total profit per year

    sales = data1

    sales12=sales.groupby(['Market','Year'])['Total Item Profit'].sum()
    sales12=sales12.to_frame().reset_index()

    sales12 = sales12[sales12['Year'].isin(position_choice)]
    sales12 = sales12[sales12['Market'].isin(position_choice2)]

    sales12a= sales12.groupby(['Year'])['Total Item Profit'].sum()
    sales12a= sales12a.to_frame().reset_index()

    fig208 = go.Figure(go.Bar(
                    x= sales12a['Year'],
                    y= sales12a['Total Item Profit'],
                    marker_color='#3cabe2',
                    opacity=0.9,
                    orientation='v'))
    fig208.update_xaxes(type='category')
    fig208.update_layout(
            title_text='Profit Per Year', # title of plot
            titlefont =dict(
                family="Arial Black",
                size=16,
                color='#000000'
            ),font=dict(
                    family="Arial",
                    size=10,
                    color='#000000'
                ),
            xaxis_title_text='', # xaxis label
            yaxis_title_text='', # yaxis label
            bargap=0.2, # gap between bars of adjacent location coordinates
    bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates
    ## Sales per market

    sales = data1

    sales13=sales.groupby(['Market','Year'])['Total Item Sale'].sum()
    sales13=sales13.to_frame().sort_values(by =['Total Item Sale'] , ascending = False).reset_index()

    sales13 = sales13[sales13['Year'].isin(position_choice)]
    sales13 = sales13[sales13['Market'].isin(position_choice2)]

    sales13['Market Share'] = sales13['Total Item Sale'] *100 / sales13['Total Item Sale'].sum()

    sales13a=sales13.groupby(['Market'])['Total Item Sale'].sum()
    sales13a=sales13a.to_frame().sort_values(by =['Total Item Sale'] , ascending = False).reset_index()


    fig209 = px.pie(sales13, values='Total Item Sale', names='Market',hole = 0.5, color_discrete_sequence=px.colors.sequential.Agsunset)
    fig209.update_traces(textposition='inside', textinfo='percent+label')
    fig209.update_layout(
                title_text='Sales Distribution by Market', # title of plot
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ),
                xaxis_title_text='Status', # xaxis label
                yaxis_title_text='', # yaxis label
                showlegend= False,
                bargap=0.2, # gap between bars of adjacent location coordinates
                bargroupgap=0.1) # gap between bars of the same location coordinates

    ## Total Sales per Top 10 Country

    sales = data1

    sales14=sales.groupby(['Order Country','Market','Year'])['Total Item Sale'].sum()
    sales14=sales14.to_frame().sort_values(by =['Total Item Sale'] , ascending = True).reset_index()

    sales14 = sales14[sales14['Year'].isin(position_choice)]
    sales14 = sales14[sales14['Market'].isin(position_choice2)]

    sales14a=sales14.groupby(['Order Country'])['Total Item Sale'].sum()
    sales14a=sales14a.to_frame().sort_values(by =['Total Item Sale'] , ascending = True).tail(10).reset_index()

    sales14b=sales14.groupby(['Order Country'])['Total Item Sale'].sum()
    sales14b=sales14b.to_frame().sort_values(by =['Total Item Sale'] , ascending = False).reset_index()

    fig210 = go.Figure(go.Bar(
                        y= sales14a['Order Country'],
                        x= sales14a['Total Item Sale'],
                        marker_color='#3cabe2',
                        opacity=0.9,
                        orientation='h'))
    fig210.update_yaxes(type='category')
    fig210.update_layout(
                title_text='Top 10 Countries Sale', # title of plot
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ),
                xaxis_title_text='', # xaxis label
                yaxis_title_text='', # yaxis label
                bargap=0.2, # gap between bars of adjacent location coordinates
                bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates

    ## Total Sales per Department

    dales = data1

    sales15=sales.groupby(['Department Name','Year','Market'])['Total Item Sale'].sum()
    sales15=sales15.to_frame().sort_values(by =['Total Item Sale'] , ascending = False).reset_index()

    sales15 = sales15[sales15['Year'].isin(position_choice)]
    sales15 = sales15[sales15['Market'].isin(position_choice2)]

    sales15a=sales15.groupby(['Department Name'])['Total Item Sale'].sum()
    sales15a=sales15a.to_frame().sort_values(by =['Total Item Sale'] , ascending = True).reset_index()

    fig211 = go.Figure(go.Bar(
                        y= sales15a['Department Name'],
                        x= sales15a['Total Item Sale'],
                        hovertext=sales15['Year'],
                        marker_color='#3cabe2',
                        opacity=0.9,
                        orientation='h'))

    fig211.update_layout(
                title_text='Sales by Department', # title of plot
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ),
                xaxis_title_text='', # xaxis label
                yaxis_title_text='', # yaxis label
                bargap=0.2, # gap between bars of adjacent location coordinates
                bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates

    ## Late delivery risk 

    sales = data1

    sales16 = sales[['Year','Market','Order Id','Late delivery risk']]
    sales16= sales16.drop_duplicates(subset='Order Id', keep='first').reset_index()

    sales16 = sales16[sales16['Year'].isin(position_choice)]
    sales16 = sales16[sales16['Market'].isin(position_choice2)]

    sales16a= sales16.groupby(['Year'])['Late delivery risk'].value_counts()
    sales16a= sales16a.to_frame().sort_values(by =['Late delivery risk'] , ascending = False).reset_index()
    sales16a['%_of_total'] = sales16a['Late delivery risk'] *100 / sales16a['Late delivery risk'].sum()

    sales16b= sales16.groupby(['Year'])['Late delivery risk'].value_counts()
    sales16b= sales16b.reset_index()
    sales16b= sales16b.groupby(['level_1'])['Late delivery risk'].sum()
    sales16b= sales16b.to_frame().sort_values(by =['Late delivery risk'] , ascending = False).reset_index()

    fig212 = px.pie(sales16a, values='Late delivery risk', names='level_1', hole = 0.5, color_discrete_sequence=px.colors.sequential.Agsunset)
    fig212.update_traces(textposition='inside', textinfo='percent+label')
    fig212.update_layout(
                title_text='Late Delivery risk',
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ), showlegend = False)
    
    ## Transaction Type

    sales = data1

    sales17 = sales[['Year','Order Id','Market','Transaction Type']]

    sales17= sales17.drop_duplicates(subset='Order Id', keep='first').reset_index()

    sales17 = sales17[sales17['Year'].isin(position_choice)]
    sales17 = sales17[sales17['Market'].isin(position_choice2)]

    sales17a= sales17.groupby(['Year'])['Transaction Type'].value_counts()
    sales17a= sales17a.to_frame().sort_values(by =['Transaction Type'] , ascending = False).reset_index()
    sales17a['%_of_total'] = sales17a['Transaction Type'] *100 / sales17a['Transaction Type'].sum()

    sales17b= sales17.groupby(['Year'])['Transaction Type'].value_counts()
    sales17b= sales17b.reset_index()
    sales17b= sales17b.groupby(['level_1'])['Transaction Type'].sum()
    sales17b= sales17b.to_frame().sort_values(by =['Transaction Type'] , ascending = False).reset_index()

    fig213 = px.pie(sales17a, values='Transaction Type', names='level_1', hole = 0.5, color_discrete_sequence=px.colors.sequential.Agsunset)
    fig213.update_traces(textposition='inside', textinfo='percent+label')
    fig213.update_layout(
                title_text='Orders by Payment Type', 
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ),showlegend = False)

    ### Sales & Profit per region

    sales = data1

    sales19=sales.groupby(['Year','Market','Order Region']).agg(Total_Sales =('Total Item Sale','sum'),Total_Profit  =('Total Item Profit','sum'))
    sales19=sales19.sort_values(by =['Total_Sales'] , ascending = True).reset_index()

    sales19 = sales19[sales19['Year'].isin(position_choice)]
    sales19 = sales19[sales19['Market'].isin(position_choice2)]

    sales19a=sales19.groupby(['Order Region'])['Total_Sales'].sum()
    sales19a=sales19a.to_frame().sort_values(by =['Total_Sales'] , ascending = False).reset_index()

    sales19b=sales19.groupby(['Order Region'])['Total_Profit'].sum()
    sales19b=sales19b.to_frame().sort_values(by =['Total_Profit'] , ascending = False).reset_index()

    fig215 = go.Figure()
    fig215.add_trace(    
                go.Bar(
                        x= sales19['Order Region'],
                        y= sales19['Total_Profit'],
                        marker_color='#e23c3c',
                        name='Total Profit',
                        opacity=0.9,
                        orientation='v'))
    fig215.add_trace(go.Bar(
                        x= sales19['Order Region'],
                        y= sales19['Total_Sales'],
                        marker_color='#3cabe2',
                        name='Total Sales',
                        opacity=0.9,
                        orientation='v'))

    fig215.update_layout(
                barmode='group', xaxis_tickangle=-45,
                title_text='Sales & Profit by Region', # title of plot
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ),
                xaxis_title_text='', # xaxis label
                yaxis_title_text='', # yaxis label
                bargap=0.2, # gap between bars of adjacent location coordinates
                bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates

    ## Orders Shipping Mode Distribution

    sales20 = sales[['Year','Market','Order Id','Shipping Mode']]
    sales20= sales20.drop_duplicates(subset='Order Id', keep='first').reset_index()

    sales20 = sales20[sales20['Year'].isin(position_choice)]
    sales20 = sales20[sales20['Market'].isin(position_choice2)]

    sales20a= sales20.groupby(['Year'])['Shipping Mode'].value_counts()
    sales20a= sales20a.to_frame().sort_values(by =['Shipping Mode'] , ascending = False).reset_index()
    sales20a['%_of_total'] = sales20a['Shipping Mode'] *100 / sales20a['Shipping Mode'].sum()

    sales20b= sales20.groupby(['Year'])['Shipping Mode'].value_counts()
    sales20b= sales20b.reset_index()
    sales20b= sales20b.groupby(['level_1'])['Shipping Mode'].sum()
    sales20b= sales20b.to_frame().sort_values(by =['Shipping Mode'] , ascending = False).reset_index()

    fig216 = px.pie(sales20a, values='Shipping Mode', names='level_1', hole = 0.5, color_discrete_sequence=px.colors.sequential.Agsunset)
    fig216.update_traces(textposition='inside', textinfo='percent+label')
    fig216.update_layout(
                title_text='Shipping Mode',
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ), showlegend = False)

    ## Top 10 Sold Products by Sales

    sales = data1

    sales22=sales.groupby(['Year','Product Name','Market'])['Total Item Sale'].sum()
    sales22=sales22.to_frame().sort_values(by =['Total Item Sale'] , ascending = True).reset_index()

    sales22 = sales22[sales22['Year'].isin(position_choice)]
    sales22 = sales22[sales22['Market'].isin(position_choice2)]

    sales22a=sales22.groupby(['Product Name'])['Total Item Sale'].sum()
    sales22a=sales22a.to_frame().sort_values(by =['Total Item Sale'] , ascending = True).tail(10).reset_index()

    sales22b=sales22.groupby(['Product Name'])['Total Item Sale'].sum()
    sales22b=sales22b.to_frame().sort_values(by =['Total Item Sale'] , ascending = False).reset_index()

    fig218 = go.Figure()
    fig218.add_trace(go.Bar(
                    y= sales22a['Product Name'],
                    x= sales22a['Total Item Sale'],
                    marker_color='#3cabe2',
                    name='Total Sales',
                    opacity=0.9,
                    orientation='h'))

    fig218.update_layout(
            barmode='group', xaxis_tickangle=-45,
            title_text='Top 10 Products by Sales', # title of plot
            titlefont =dict(
                family="Arial Black",
                size=16,
                color='#000000'
            ),font=dict(
                    family="Arial",
                    size=10,
                    color='#000000'
                ),
            xaxis_title_text='', # xaxis label
            yaxis_title_text='', # yaxis label
            bargap=0.2, # gap between bars of adjacent location coordinates
            bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates

    ## Top 10 Sold Products by Profit

    sales = data1

    sales23=sales.groupby(['Year','Product Name','Market'])['Total Item Profit'].sum()
    sales23=sales23.to_frame().sort_values(by =['Total Item Profit'] , ascending = True).reset_index()

    sales23 = sales23[sales23['Year'].isin(position_choice)]
    sales23 = sales23[sales23['Market'].isin(position_choice2)]

    sales23a=sales23.groupby(['Product Name'])['Total Item Profit'].sum()
    sales23a=sales23a.to_frame().sort_values(by =['Total Item Profit'] , ascending = True).tail(10).reset_index()

    sales23b=sales23.groupby(['Product Name'])['Total Item Profit'].sum()
    sales23b=sales23b.to_frame().sort_values(by =['Total Item Profit'] , ascending = False).reset_index()

    fig219 = go.Figure()
    fig219.add_trace(go.Bar(
                    y= sales23a['Product Name'],
                    x= sales23a['Total Item Profit'],
                    marker_color='#3cabe2',
                    name='Total Profit',
                    opacity=0.9,
                    orientation='h'))

    fig219.update_layout(
            barmode='group', xaxis_tickangle=-45,
            title_text='Top 10 Products by Profit', # title of plot
            titlefont =dict(
                family="Arial Black",
                size=16,
                color='#000000'
            ),font=dict(
                    family="Arial",
                    size=10,
                    color='#000000'
                ),
            xaxis_title_text='', # xaxis label
            yaxis_title_text='', # yaxis label
            bargap=0.2, # gap between bars of adjacent location coordinates
            bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates

    ## Tree map for Sales across Market, region & Country

    sales = data1
    sales25 = sales[['Year','Order Region','Market','Order Country','Total Item Sale']]

    sales25 = sales25[sales25['Year'].isin(position_choice)]
    sales25 = sales25[sales25['Market'].isin(position_choice2)]

    fig221 = px.treemap(sales25, path=[px.Constant("World"),'Market', 'Order Region','Order Country'], values= 'Total Item Sale',
                    color='Market',
                    color_continuous_scale='RdBu')

    fig221.update_layout(margin = dict(t=50, l=25, r=25, b=25),title_text='Sales by Market, Region, & Country',
            titlefont =dict(
            family="Arial Black",
            size=16,
            color='#000000'
        ),font=dict(
                family="Arial",
                size=10,
                color='#000000'
            ))

    ## Orders Delivery Status

    sales = data1
    sales26 = sales[['Year','Market','Order Id','Delivery Status']]
    sales26= sales26.drop_duplicates(subset='Order Id', keep='first').reset_index()

    sales26 = sales26[sales26['Year'].isin(position_choice)]
    sales26 = sales26[sales26['Market'].isin(position_choice2)]

    sales26a= sales26.groupby(['Year'])['Delivery Status'].value_counts()
    sales26a= sales26a.to_frame().sort_values(by =['Delivery Status'] , ascending = False).reset_index()
    sales26a['%_of_total'] = sales26a['Delivery Status'] *100 / sales26a['Delivery Status'].sum()

    sales26b= sales26.groupby(['Year'])['Delivery Status'].value_counts()
    sales26b= sales26b.reset_index()
    sales26b= sales26b.groupby(['level_1'])['Delivery Status'].sum()
    sales26b= sales26b.to_frame().sort_values(by =['Delivery Status'] , ascending = False).reset_index()

    fig222 = px.funnel(sales26b, x='Delivery Status', y='level_1',opacity=0.9)
    fig222.update_layout(
                title_text='Delivery Status', # title of plot
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ),
                xaxis_title_text='', 
                yaxis_title_text='')

    ### Sales by product Category Name

    sales = data1

    sales27=sales.groupby(['Year','Category Name','Market'])['Total Item Sale'].sum()
    sales27=sales27.to_frame().sort_values(by =['Total Item Sale'] , ascending = True).reset_index()

    sales27 = sales27[sales27['Year'].isin(position_choice)]
    sales27 = sales27[sales27['Market'].isin(position_choice2)]

    sales27a=sales27.groupby(['Category Name'])['Total Item Sale'].sum()
    sales27a=sales27a.to_frame().sort_values(by =['Total Item Sale'] , ascending = True).tail(10).reset_index()

    sales27b=sales27.groupby(['Category Name'])['Total Item Sale'].sum()
    sales27b=sales27b.to_frame().sort_values(by =['Total Item Sale'] , ascending = False).reset_index()

    fig223 = go.Figure()
    fig223.add_trace(go.Bar(
                    y= sales27a['Category Name'],
                    x= sales27a['Total Item Sale'],
                    marker_color='#3cabe2',
                    name='Total Sales',
                    opacity=0.9,
                    orientation='h'))

    fig223.update_layout(
            barmode='group', xaxis_tickangle=-45,
            title_text='Top 10 Product Category by Sales', # title of plot
            titlefont =dict(
                family="Arial Black",
                size=16,
                color='#000000'
            ),font=dict(
                    family="Arial",
                    size=10,
                    color='#000000'
                ),
            xaxis_title_text='', # xaxis label
            yaxis_title_text='', # yaxis label
            bargap=0.2, # gap between bars of adjacent location coordinates
            bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates

    ### Profit by product Category Name

    sales = data1

    sales28=sales.groupby(['Year','Category Name','Market'])['Total Item Profit'].sum()
    sales28=sales28.to_frame().sort_values(by =['Total Item Profit'] , ascending = True).reset_index()

    sales28 = sales28[sales28['Year'].isin(position_choice)]
    sales28 = sales28[sales28['Market'].isin(position_choice2)]

    sales28a=sales28.groupby(['Category Name'])['Total Item Profit'].sum()
    sales28a=sales28a.to_frame().sort_values(by =['Total Item Profit'] , ascending = True).tail(10).reset_index()

    sales28b=sales28.groupby(['Category Name'])['Total Item Profit'].sum()
    sales28b=sales28b.to_frame().sort_values(by =['Total Item Profit'] , ascending = False).reset_index()

    fig224 = go.Figure()
    fig224.add_trace(go.Bar(
                    y= sales28a['Category Name'],
                    x= sales28a['Total Item Profit'],
                    marker_color='#3cabe2',
                    name='Total Profit',
                    opacity=0.9,
                    orientation='h'))

    fig224.update_layout(
            barmode='group', xaxis_tickangle=-45,
            title_text='Top 10 Product Category by Profit', # title of plot
            titlefont =dict(
                family="Arial Black",
                size=16,
                color='#000000'
            ),font=dict(
                    family="Arial",
                    size=10,
                    color='#000000'
                ),
            xaxis_title_text='', # xaxis label
            yaxis_title_text='', # yaxis label
            bargap=0.2, # gap between bars of adjacent location coordinates
            bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates

    ## Orders by Status

    sales = data1

    sales30 = sales[['Year','Market','Order Id','Order Status']]
    sales30= sales30.drop_duplicates(subset='Order Id', keep='first').reset_index()

    sales30 = sales30[sales30['Year'].isin(position_choice)]
    sales30 = sales30[sales30['Market'].isin(position_choice2)]

    sales30a= sales30.groupby(['Year'])['Order Status'].value_counts()
    sales30a= sales30a.to_frame().sort_values(by =['Order Status'] , ascending = False).reset_index()
    sales30a['%_of_total'] = sales30a['Order Status'] *100 / sales30a['Order Status'].sum()


    sales30b= sales30.groupby(['Year'])['Order Status'].value_counts()
    sales30b= sales30b.reset_index()
    sales30b= sales30b.groupby(['level_1'])['Order Status'].sum()
    sales30b= sales30b.to_frame().sort_values(by =['Order Status'] , ascending = False).reset_index()


    fig226 = px.funnel(sales30b, x='Order Status', y='level_1',opacity=0.9)
    fig226.update_layout(
                title_text='Orders Status', # title of plot
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ),
                xaxis_title_text='', 
                yaxis_title_text='')

    ### Top 10 Customers by Sales Value

    sales = data1
    sales['Customer Name (ID)'] = sales['Customer Name'].astype(str) + " (" +  sales['Customer Id'].astype(str) + ")"

    sales31=sales.groupby(['Year','Customer Name (ID)','Market'])['Total Item Sale'].sum()
    sales31=sales31.to_frame().sort_values(by =['Total Item Sale'] , ascending = True).reset_index()

    sales31 = sales31[sales31['Year'].isin(position_choice)]
    sales31 = sales31[sales31['Market'].isin(position_choice2)]

    sales31a=sales31.groupby(['Customer Name (ID)'])['Total Item Sale'].sum()
    sales31a=sales31a.to_frame().sort_values(by =['Total Item Sale'] , ascending = True).tail(10).reset_index()

    sales31b=sales31.groupby(['Customer Name (ID)'])['Total Item Sale'].sum()
    sales31b=sales31b.to_frame().sort_values(by =['Total Item Sale'] , ascending = False).reset_index()

    fig227 = go.Figure(go.Bar(
                        y= sales31a['Customer Name (ID)'],
                        x= sales31a['Total Item Sale'],
                        marker_color='#3cabe2',
                        opacity=0.9,
                        orientation='h'))
    fig227.update_yaxes(type='category')
    fig227.update_layout(
                title_text='Top 10 Customers by Sales Value', # title of plot
                titlefont =dict(
                    family="Arial Black",
                    size=16,
                    color='#000000'
                ),font=dict(
                        family="Arial",
                        size=10,
                        color='#000000'
                    ),
                xaxis_title_text='', # xaxis label
                yaxis_title_text='', # yaxis label
                bargap=0.2, # gap between bars of adjacent location coordinates
                bargroupgap=0.1,xaxis_showgrid=False, yaxis_showgrid=False) # gap between bars of the same location coordinates

    ## Streamlit Layout

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 300px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 500px;
            margin-left: -500px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    
    genre = st.radio('Sections',
        ('Main','Sales', 'Orders', 'Products','Delivery'))

    if genre == 'Main':
        st.write('')

    elif genre == 'Sales':
        st.subheader('You are reviewing a general overview of the business performance.')

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        kpi1.metric(
        label="Total Sales 📊",
        value='{:,.2f}'.format(sales2['Total Item Sale'].sum()))

        kpi2.metric(
        label="Total Profit 💰",
        value='{:,.2f}'.format(sales12['Total Item Profit'].sum()))

        kpi3.metric(
        label=" Profit Margin %",
        value='{:,.2f}'.format(sales12['Total Item Profit'].sum()*100/sales2['Total Item Sale'].sum()))

        kpi4.metric(
        label="Total Discount 💵",
        value='{:,.2f}'.format(sales5['Order Item Discount'].sum()))

        c11,c12 = st.columns((1,1))
        with c11:
            st.write(fig207)

        with c12:
            st.write(fig208)
        
        col1, col2, col3 = st.columns([2,6,2])
        
        with col1:
            st.write("")

        with col2:
            
            st.write(fig209)

            first_market = sales13a['Market'].iloc[0]
            last_market = sales13a['Market'].iloc[-1]

            first_market_a = sales13.loc[sales13['Market'] == first_market,['Total Item Sale']]
            first_sales = first_market_a['Total Item Sale'].sum()
            last_market_a = sales13.loc[sales13['Market'] == last_market,['Total Item Sale']]
            last_sales = last_market_a['Total Item Sale'].sum()

            first_market_a1 = sales13.loc[sales13['Market'] == first_market,['Market Share']]
            first_value = first_market_a1['Market Share'].sum()
            last_market_a1 = sales13.loc[sales13['Market'] == last_market,['Market Share']]
            last_value = last_market_a1['Market Share'].sum()

            st.write(f'The highest market share in terms of sales was **{first_market}**'+ ' with a total sales of ' + '**{:,.2f}**'.format(first_sales) + ' and a market share value of '
                                    + '**{:,.1f}**'.format(first_value) +'%' )

        with col3:
            st.write("")

        c110,c120 = st.columns((1,1))

        with c110:

            st.write(fig210)

            first_country = sales14a['Order Country'].iloc[-1]
            second_country = sales14a['Order Country'].iloc[-2]
            third_country = sales14a['Order Country'].iloc[-3]

            max1 = sales14.loc[sales14['Order Country'] == first_country,['Total Item Sale']]
            total_sales = max1['Total Item Sale'].sum()

            st.write(f'The top 3 countries in terms of sales recorded were **{first_country}**, **{second_country}**, & **{third_country}** respectively, where the **{first_country}** scored the highest numnber in terms of sales with a total value of '
                                    + '**{:,.2f}**'.format(total_sales))

        with c120:

            st.write(fig211) 

            first_depart = sales15a['Department Name'].iloc[-1]
            second_depart = sales15a['Department Name'].iloc[-2]
            lowest_depart = sales15a['Department Name'].iloc[0]

            max1 = sales15.loc[sales15['Department Name'] == first_depart,['Total Item Sale']]
            total_sales = max1['Total Item Sale'].sum()
            low1 = sales15.loc[sales15['Department Name'] == lowest_depart,['Total Item Sale']]
            total_sales1 = low1['Total Item Sale'].sum()

            st.write(f'As for the top 2 departments in terms of sales, **{first_depart}** and **{second_depart}** recorded the highest numbers with the **{first_depart}** department recording a total amount of '
                                    +'**{:,.2f}**'.format(total_sales))
            st.write(f'On the other side **{lowest_depart}** recorded the lowest sales numbers with a total amount of '
                                    +'**{:,.2f}**'.format(total_sales1))   

    elif genre == 'Orders':
        st.subheader('You are reviewing the orders section')

        kpi1a, kpi2a, kpi3a, kpi4a = st.columns(4)
        
        kpi1a.metric(
        label="Total Orders",
        value='{:,.0f}'.format(sales6a))

        kpi2a.metric(
        label="Total Ordered Quantities",
        value='{:,.0f}'.format(sales7['Ordered Quantity'].sum()))

        kpi3a.metric(
        label=" Average Order Value",
        value='{:,.2f}'.format(sales2['Total Item Sale'].sum()/sales6a))

        kpi4a.metric(
        label="Average Order Profit",
        value='{:,.2f}'.format(sales12['Total Item Profit'].sum()/sales6a))


        c101,c102 = st.columns((1,1))

        with c101:

            st.write(fig215)

            first_region_sales = sales19a['Order Region'].iloc[0]
            second_region_sales = sales19a['Order Region'].iloc[1]
            third_region_sales = sales19a['Order Region'].iloc[2]     
            least_region_sales = sales19a['Order Region'].iloc[-1]

            first_region_profit = sales19b['Order Region'].iloc[0]
            second_region_profit = sales19b['Order Region'].iloc[1]
            third_region_profit = sales19b['Order Region'].iloc[2]   
            least_region_profit = sales19b['Order Region'].iloc[-1]

            max_sales = sales19.loc[sales19['Order Region'] == first_region_sales,['Total_Sales']]
            total_sales = max_sales['Total_Sales'].sum()
            low_sales = sales19.loc[sales19['Order Region'] == least_region_sales,['Total_Sales']]
            total_sales1 = low_sales['Total_Sales'].sum()

            max_profit = sales19.loc[sales19['Order Region'] == first_region_profit,['Total_Profit']]
            total_profit = max_profit['Total_Profit'].sum()
            low_profit = sales19.loc[sales19['Order Region'] == least_region_profit,['Total_Profit']]
            total_profit1 = low_profit['Total_Profit'].sum()

            st.write(f' In terms of sales and profit per region, our top 3 regions were **{first_region_sales}**, **{second_region_sales}**, & **{third_region_sales}** respectively, where the **{first_region_sales}** scored the highest numbers in terms of both profit and sales with respective values of '
                                    + '**{:,.2f}**'.format(total_sales) + ' for sales and ' + '**{:,.2f}**'.format(total_profit) + ' for profit.')  
            st.write(f' On the opposite side, **{least_region_sales}** recorded the lowest number in terms of sales with the respective values of '
                                    + '**{:,.2f}**'.format(total_sales1) + f' and **{least_region_profit}** recorded the lowest number in terms of profit with' + '**{:,.2f}**'.format(total_profit1))

        with c102:

            st.write(fig227)

            first_customer = sales31a['Customer Name (ID)'].iloc[-1]

            max_customer = sales31.loc[sales31['Customer Name (ID)'] == first_customer,['Total Item Sale']]
            total_sales_cus = max_customer['Total Item Sale'].sum()

            st.write(f' Looking at the above plot, we can see that our top 10 customers in terms of sales were relatively close to each other, where **{first_customer}** had the highest amount of goods purchased with a respective value of '
                                    + '**{:,.2f}**'.format(total_sales_cus))
                

        col4, col5, col6 = st.columns([2,6,2])
        
        with col4:
            st.write("")
        with col5:
            st.write(fig221)

            st.write(f'To dig deeper into the orders sales by country, the above treemap shows us how the sales were distributed respectively across the market, region, and its corresponding countries.')
        with col6:
            st.write("")           
        
        c151,c161 = st.columns((1,1))

        with c151:

            st.write(fig226)

            top_status= sales30b['level_1'].iloc[0]
            top_value12 = sales30a.loc[sales30a['level_1'] == top_status,['%_of_total']]
            first_value12 = top_value12['%_of_total'].sum()

            st.write(f'Looking at the above funnel, we can see that only ' + '**{:,.2f}**'.format(first_value12) +'%' + f' of our orders were **{top_status}** compared to the rest orders type.')
            st.write('This indicates that we must look deeper behind the reasons of why so many orders are either not completed, cancelled or on-hold')

        with c161:

            st.write(fig213)

            top_payment= sales17b['level_1'].iloc[0]
            top_value = sales17a.loc[sales17a['level_1'] == top_payment,['%_of_total']]
            first_value = top_value['%_of_total'].sum()

            st.write(f'In terms of types of payment made by the customers, we can notice that our top category was **{top_payment}** with a respective total of '+
                        "%s%%"%'**{:,.2f}**'.format(first_value) + ' out of all methods used by the customers to pay for their orders.')
        
    
    elif genre == 'Products':
        st.subheader('You are reviewing the products summary section')

        kpi1a1, kpi2a1, kpi3a1, kpi4a1 = st.columns([1,1,1,2])
        
        first_Category= sales27a['Category Name'].iloc[-1]
        kpi1a1.metric(
        label="Top Category by Sales",
        value=first_Category)
        
        least_Category = sales27b['Category Name'].iloc[-1]
        kpi2a1.metric(
        label="Least Category by Sales",
        value=least_Category)

        first_Category11= sales22a['Product Name'].iloc[-1]
        kpi4a1.metric(
        label="Top Sold Product",
        value=first_Category11)

        kpi3a1.metric(
        label="Distinct Products Ordered",
        value='{:,.0f}'.format(sales8a))

        c301,c302 = st.columns((1,1))
        with c301:

            st.write(fig223)

            first_Category= sales27a['Category Name'].iloc[-1]
            second_Category = sales27a['Category Name'].iloc[-2]
            third_Category= sales27a['Category Name'].iloc[-3]     
            least_2_Category = sales27b['Category Name'].iloc[-2]
            least_Category = sales27b['Category Name'].iloc[-1] 

                        
            top_sales = sales27b.loc[sales27b['Category Name'] == first_Category,['Total Item Sale']]
            top_value = top_sales['Total Item Sale'].sum()
            
            least_sales = sales27b.loc[sales27b['Category Name'] == least_Category,['Total Item Sale']]
            least_value = least_sales['Total Item Sale'].sum()           
                        
            st.write(f' In terms of sales per category name, the top 3 categories were **{first_Category}**, **{second_Category}**, & **{third_Category}** respectively, where the **{first_Category}** scored the highest number in terms of sales with a respective value of '
                        + '**{:,.2f}**'.format(top_value))  
            st.markdown(f' On the opposite side, **{least_2_Category}** & **{least_Category}** recorded the lowest numbers in sales per category, where **{least_Category}** had the lowest sales values of '
                        + '**{:,.2f}**'.format(least_value))


        with c302:

            st.write(fig224)

            first_Category1= sales28a['Category Name'].iloc[-1]
            second_Category1 = sales28a['Category Name'].iloc[-2]
            third_Category1= sales28a['Category Name'].iloc[-3]     
            least_2_Category1 = sales28b['Category Name'].iloc[-2]
            least_Category1 = sales28b['Category Name'].iloc[-1] 

            top_profit = sales28b.loc[sales28b['Category Name'] == first_Category1,['Total Item Profit']]
            top_value1 = top_profit['Total Item Profit'].sum()
            least_profit = sales28b.loc[sales28b['Category Name'] == least_Category1,['Total Item Profit']]
            least_value1 = least_profit['Total Item Profit'].sum() 
                        
            st.write(f' As for the profit per category, the top 3 categories were **{first_Category1}**, **{second_Category1}**, & **{third_Category1}** respectively, where the **{first_Category1}** scored the highest number in terms of profit with a respective value of '
                                    + '**{:,.2f}**'.format(top_value1))  
            st.write(f' On the other side, **{least_2_Category1}** & **{least_Category1}** recorded the lowest numbers in profit per category, where **{least_Category1}** had the lowest profit values of '
                                    + '**{:,.2f}**'.format(least_value1))

        c312,c313 = st.columns((1,1))

        with c312:

            st.write(fig218)    

            first_Category11= sales22a['Product Name'].iloc[-1]
            second_Category11 = sales22a['Product Name'].iloc[-2]
            third_Category11= sales22a['Product Name'].iloc[-3]     
            least_2_Category11 = sales22b['Product Name'].iloc[-2]
            least_Category11 = sales22b['Product Name'].iloc[-1] 

            top_sales1 = sales22b.loc[sales22b['Product Name'] == first_Category11,['Total Item Sale']]
            top_value11 = top_sales1['Total Item Sale'].sum()
            least_sales1 = sales22b.loc[sales22b['Product Name'] == least_Category11,['Total Item Sale']]
            least_value11 = least_sales1['Total Item Sale'].sum() 
                        
            st.write(f' In terms of sales by product, the top 3 products were **{first_Category11}**, **{second_Category11}**, & **{third_Category11}** respectively, where the **{first_Category11}** scored the highest number in terms of sales with a respective value of '
                                    + '**{:,.2f}**'.format(top_value11))  
            st.write(f' On the opposite side, **{least_2_Category11}** & **{least_Category11}** recorded the lowest numbers in the sales per product, where **{least_Category11}** had the lowest sales values of '
                                    + '**{:,.2f}**'.format(least_value11))

        with c313:

            st.write(fig219)

            first_Category111= sales23a['Product Name'].iloc[-1]
            second_Category111 = sales23a['Product Name'].iloc[-2]
            third_Category111= sales23a['Product Name'].iloc[-3]     
            least_2_Category111 = sales23b['Product Name'].iloc[-2]
            least_Category111 = sales23b['Product Name'].iloc[-1] 

            top_profit11 = sales23b.loc[sales23b['Product Name'] == first_Category111,['Total Item Profit']]
            top_value111 = top_profit11['Total Item Profit'].sum()
            least_profit11 = sales23b.loc[sales23b['Product Name'] == least_Category111,['Total Item Profit']]
            least_value111 = least_profit11['Total Item Profit'].sum() 
                        
            st.write(f' In terms of profit by product, the top 3 profitable products were **{first_Category111}**, **{second_Category111}**, & **{third_Category111}** respectively, where the **{first_Category111}** the highest profit  value of '
                                    + '**{:,.2f}**'.format(top_value111))  
            st.write(f' On the other side, **{least_2_Category111}** & **{least_Category111}** recorded the lowest numbers in the profit per product, where **{least_Category111}** had the lowest profit values of '
                                    + '**{:,.2f}**'.format(least_value111))

    else:
        st.subheader('You are reviewing the orders delivery status')

        c401,c402 = st.columns((1,1))
        with c401:

            st.write(fig212)

            risk_yes1 = sales16b['level_1'].iloc[0]
            no_risk1 = sales16b['level_1'].iloc[-1]

            yes_values = sales16a.loc[sales16a['level_1'] == risk_yes1,['%_of_total']]
            first_value = yes_values['%_of_total'].sum()
            no_values = sales16a.loc[sales16a['level_1'] == no_risk1,['%_of_total']]
            last_value = no_values['%_of_total'].sum()

            st.write(f'The above pie chart shows us that the biggest part of our orders had a delivery risk **{risk_yes1}**'+ ' with a total percentage of '
                                    + '**{:,.1f}**'.format(first_value) +'%.')
            st.write(f'On the other side, the orders with a delivery risk labeled as **{no_risk1}** had with a total percentage of ' 
                                    + '**{:,.2f}**'.format(last_value)+'%')

        with c402:

            st.write(fig216)

            most_type = sales20b['level_1'].iloc[0]
            least_type = sales20b['level_1'].iloc[-1]

            yes_values1 = sales20a.loc[sales20a['level_1'] == most_type,['%_of_total']]
            first_value1 = yes_values1['%_of_total'].sum()
            no_values1 = sales20a.loc[sales20a['level_1'] == least_type,['%_of_total']]
            least_value1 = no_values1['%_of_total'].sum()

            st.write(f'In terms of orders shipping mode,  **{most_type}**'+ ' had the highest percentage among all the other types with a total percentage of '
                        + '**{:,.1f}**'.format(first_value1) +'%.')
            st.write(f'On the least adopted mode of shipment was **{least_type}** had with a total percentage of ' 
                        + '**{:,.2f}**'.format(least_value1)+'%.'+f' Not much orders were shipped on **{least_type}**')

        col414, col415, col416 = st.columns([2,6,2])
        
        with col414:
            st.write("")

        with col415:
            
            st.write(fig222)

            top_status= sales26b['level_1'].iloc[0]
            top_value1 = sales26b.loc[sales26b['level_1'] == top_status,['Delivery Status']]
            first_value1 = top_value1['Delivery Status'].sum()
            top_value12 = sales26a.loc[sales26a['level_1'] == top_status,['%_of_total']]
            first_value12 = top_value12['%_of_total'].sum()

            st.write(f'Looking at the above funnel, we can see that ' + '**{:,.2f}**'.format(first_value12) +'%' + f' of our orders were **{top_status}** compared to the rest orders type.')
            if top_status == 'Late delivery':
                st.write(f'This indicates that we must look deeper why so many orders are on {top_status} status')
            else:
                st.write('')

        with col416:
            st.write("")
