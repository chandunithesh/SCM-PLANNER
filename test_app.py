import unittest
import os
import pandas as pd
from app import app, process_data, save_schedule_to_pickle, load_schedule_from_pickle

class FlaskAppTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_all_files(self):
        # Simulate file upload with valid files
        with open('test_orders.csv', 'w') as f:
            f.write("OrderID,Quantity\n1,10\n2,20")
        with open('test_inventory.csv', 'w') as f:
            f.write("ItemID,Stock\n1,100\n2,200")
        with open('test_sales_forecast.csv', 'w') as f:
            f.write("Month,Forecast\n1,30\n2,40")

        with open('test_orders.csv', 'rb') as orders_file, \
             open('test_inventory.csv', 'rb') as inventory_file, \
             open('test_sales_forecast.csv', 'rb') as sales_file:
            response = self.app.post('/upload', data={
                'Orders': orders_file,
                'Inventory': inventory_file,
                'SFC': sales_file
            })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('schedule', response.json)

    def test_upload_missing_files(self):
        # Simulate file upload with missing files
        response = self.app.post('/upload', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_process_data(self):
        # Test the process_data function directly
        orders_df = pd.DataFrame({'OrderID': [1, 2], 'Quantity': [10, 20]})
        inventory_df = pd.DataFrame({'ItemID': [1, 2], 'Stock': [100, 200]})
        sales_forecast_df = pd.DataFrame({'Month': [1, 2], 'Forecast': [30, 40]})

        schedule_df = process_data(orders_df, inventory_df, sales_forecast_df)
        self.assertEqual(len(schedule_df), 6)  # Check if it generates 6 months of schedule

    def test_save_load_pickle(self):
        # Test saving and loading from pickle
        df = pd.DataFrame({'test': [1, 2, 3]})
        save_schedule_to_pickle(df)
        loaded_df = load_schedule_from_pickle()
        pd.testing.assert_frame_equal(df, loaded_df)

    def test_load_nonexistent_pickle(self):
        # Test loading from a non-existent pickle file
        if os.path.exists("model.pkl"):
            os.remove("model.pkl")  # Ensure the file does not exist
        loaded_df = load_schedule_from_pickle()
        self.assertIsNone(loaded_df)

if __name__ == '__main__':
    unittest.main()
