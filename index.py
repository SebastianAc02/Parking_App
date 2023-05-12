from dash import Dash 
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image



from datetime import datetime
import openpyxl

EXCEL_PATH = "./carparkinglot.xlsx"
 
class Parking_Lot:
    def  __init__(self,max_opcupation):
        self.max_ocupation = max_ocupation
        self.current_ocupation = 0 
        
    
    def addVehicle(self, vehicle):
        print("hello world ")
         #check if the vehicle is ok to get into thu licence plate

    def exitVehicle(self, vehicle):
        print("something ")

    def isVehicleRegistered(self):
        print("heloo world") 
        
    def ifFull(self):
        return self.current_ocupation >= self.max_ocupation 

    def getVehicles(self):
        return [
    {"Row": 1, "Column": 1, "Occupied": 0},
    {"Row": 1, "Column": 2, "Occupied": 1},
    {"Row": 1, "Column": 3, "Occupied": 0},
    {"Row": 1, "Column": 4, "Occupied": 0},
    {"Row": 2, "Column": 1, "Occupied": 1},
    {"Row": 2, "Column": 2, "Occupied": 1},
    {"Row": 2, "Column": 3, "Occupied": 0},
    {"Row": 2, "Column": 4, "Occupied": 1},
    # ... more entries for each parking space ...
    ]



class Vehicle:
    def __init__(self, type, plate):
        self.type = type
        self.plate = plate
        self.entryHour = getHourNow()

    


    def getHourNow(self):
        ahora = datetime.now()
        fecha_hora = ahora.strftime("%Y-%m-%d %H:%M:%S")
        return fecha_hora






class ServerGPT:

    def __init__(self, name, app):
        self.app = app
        self.app_name = name
        self.file_to_watch = EXCEL_PATH
        self.layout = self.create_layout()
        self.set_callbacks()

    def create_layout(self):
        layout = html.Div([
            html.H1(f"{self.app_name}"),
            dcc.Dropdown(
                id="space_selector",
                options=[
                    {"label": "Space A", "value": "A"},
                    {"label": "Space B", "value": "B"},
                ],
                value="A",
            ),
            dcc.Graph(id="parking_lot"),  # Updated to use a Graph
            html.Div([
                dcc.Input(id="plate_input", type="text", placeholder="Plate"),
                dcc.Dropdown(
                    id="type_selector",
                    options=[
                        {"label": "Car", "value": "car"},
                        {"label": "Bike", "value": "bike"},
                    ],
                    value="car",
                ),
                html.Button('Done', id='submit-button', n_clicks=0),
            ]),
            html.Div(id="output_text"),
            dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),  # 1 second
        ])

        return layout

        import matplotlib.pyplot as plt

     

    def set_callbacks():
        def generate_parking_lot_graph():
            fig, ax = plt.subplots()
            
            rows = 5
            columns = 8
            space_between_rows = 1
            
            # Set the plot limits based on the number of rows and columns
            ax.set_xlim(0, columns)
            ax.set_ylim(0, rows * (space_between_rows + 1))
            
            # Create the cell stalls
            for row in range(rows):
                for column in range(columns):
                    cell_x = column
                    cell_y = row * (space_between_rows + 1)
                    rect = plt.Rectangle((cell_x, cell_y), 1, 1, facecolor='white', edgecolor='black')
                    ax.add_patch(rect)
            
            # Customize the plot appearance
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            plt.box(False)
            
            return fig

        @app.callback(
            Output('parking_lot', 'figure'),
            [Input('submit-button', 'n_clicks')],
            [State('plate_input', 'value'),
            State('type_selector', 'value'),
            State('row_input', 'value'),
            State('column_input', 'value')]
        )

        def add_car_to_parking_lot(n_clicks, plate, vehicle_type, row, column):
            if n_clicks and n_clicks > 0:
                # Perform the logic to add the car to the parking lot data
                # For example, you can update a data structure or an Excel file
                
                # Generate the new graph with the updated parking lot data
                updated_parking_lot = generate_parking_lot_graph()

                # Load the car image
                car_image = Image.open("bmw.jpg")
                
                # Calculate the coordinates of the cell based on row and column
                cell_x = int(column) - 1
                cell_y = int(row) - 1
                
                # Calculate the size of the cell based on the graph dimensions
                graph_width, graph_height = updated_parking_lot.get_size_inches()
                cell_width = graph_width / columns
                cell_height = graph_height / (rows * (space_between_rows + 1))
                
                # Calculate the position and size of the image within the cell
                image_x = cell_x * cell_width
                image_y = cell_y * cell_height
                image_width = cell_width
                image_height = cell_height
                
                # Add the car image to the parking lot graph
                ax = updated_parking_lot.axes[0]
                ax.imshow(car_image, extent=(image_x, image_x + image_width, image_y, image_y + image_height), aspect='auto')
                
                return updated_parking_lot

            raise dash.exceptions.PreventUpdate

        
     

    def run(self, debug=False):
        self.app.layout = self.layout
        self.app.run_server(debug=debug)

class Excel:


    def __init__(self, HEAD):

        
        self.excel_path = EXCEL_PATH
        self.excel = openpyxl.load_workbook(self.excel_path)
        self.sheet = self.excel.active

        self.headers =  list(HEAD.__dict__.keys())
        #get the index of the header where column is isparking
        self.parking_column_index = None
        try:
            self.parking_column_index = self.headers.index('isParking')+1
        except:
            pass

        #create column headers
        self.sheet.append(self.headers)
        self.excel.save(self.excel_path)

    def open_car(self, obj):
        row.data= list(vars(obj).values())
        self.sheet.append(row_data)
        self.excel.save(self.excel_path)

    def close_car(self, plate):


        if self.parking_column_index is not None:
            for row in self.sheet.iter_rows(min_row=2, values_only=True):
                if row[0] == plate:
                    row_index = seelf.sheet.index(row)+2
                    self.sheet.cell(row=row_index, column=self.parking_column_index, value =False)
                    self.excel.save(self.excel_path)
                    break
                else:
                    print("plate was not found")
        else:
            print("Error in close_car definition, not column index found ")

    def get_car_by_plate(self, plate):

        if self.parking_column_index is not None:
            for row in self.sheet.iter_rows(min_row=2 , values_only=True):
                if row[0] == plate and row[self.parking_column_index -1]:
                    car_data = {}
                    for i, header in enumerate(self.headers):
                        car_data[header] = row[i]
                    return car_data
        else:
            return None 

    def is_car_parked(self, plate):
         for row in self.sheet.iter_rows(min_row=2, values_only=True):
            if row[0] == plate and row[self.parking_column_index-1]:
                return true 
         return false

 

# Create a Dash application object
app = Dash(__name__)

# Create an instance of your Server class
server = ServerGPT("My Parking Lot App", app)

# Run the Dash application
server.run(debug=True)
