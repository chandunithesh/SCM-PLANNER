import unittest
import pandas as pd
from production_planner import calculate_production_schedule, sales_forecasting, optimize_inventory

class TestProductionPlannerIntegration(unittest.TestCase):
    def test_end_to_end_workflow(self):
        # Sample order and sales data
        orders_data = {
            'ORDER_ID': [1, 2],
            'PRODUCT_ID': ['product_1', 'product_2'],
            'PRODUCT_NAME': ['Battery A', 'Battery B'],
            'QUANTITY': [100, 200],
            'ORDER_DATE': ['2024-01-01', '2024-01-02']
        }
        orders_df = pd.DataFrame(orders_data)
        orders_df['ORDER_DATE'] = pd.to_datetime(orders_df['ORDER_DATE'])
        
        inventory_data = {
            'PRODUCT_ID': ['product_1', 'product_2'],
            'LEAD_TIME': [5, 10]
        }
        inventory_df = pd.DataFrame(inventory_data)
        
        # Merge orders with inventory
        order_inventory_df = pd.merge(orders_df, inventory_df[['PRODUCT_ID', 'LEAD_TIME']], on='PRODUCT_ID', how='left')
        
        # Simulate production scheduling for each order
        final_schedule = []
        for index, row in order_inventory_df.iterrows():
            order_quantity = row['QUANTITY']
            order_date = row['ORDER_DATE']
            lead_time_days = row['LEAD_TIME']
            schedule, lead_time_completion_date = calculate_production_schedule(order_quantity, order_date, lead_time_days)
            
            for entry in schedule:
                final_schedule.append({
                    'Order No': row['ORDER_ID'],
                    'Item Code': row['PRODUCT_ID'],
                    'Item Description': row['PRODUCT_NAME'],
                    'Order Quantity': row['QUANTITY'],
                    'Lead Time (days)': lead_time_days,
                    'Lead Time Completion Date': lead_time_completion_date,
                    'Production Date': entry['Production Date'],
                    'Minutes Used': entry['Minutes Used']
                })
        
        final_schedule_df = pd.DataFrame(final_schedule)
        
        # Check if the production schedule is generated correctly
        self.assertGreater(len(final_schedule_df), 0)  # Ensure the schedule isn't empty
        
        # Forecast sales
        sales_forecast_data = {
            'DATE': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'FORCASTED_SALES': [100, 150, 200]
        }
        sales_df = pd.DataFrame(sales_forecast_data)
        sales_df['DATE'] = pd.to_datetime(sales_df['DATE'])
        
        # Perform forecasting and check if MSE is computed
        sales_forecasting(sales_df)
        
        # Optimize inventory based on forecasted sales
        current_inventory = {'product_1': 500, 'product_2': 300}
        predicted_sales = {'product_1': 600, 'product_2': 400}
        optimal_inventory = optimize_inventory(current_inventory, predicted_sales)
        
        # Check if inventory optimization returns correct results
        self.assertEqual(optimal_inventory['product_1'], 100)
        self.assertEqual(optimal_inventory['product_2'], 100)

if __name__ == "__main__":
    unittest.main()
