# VendorTrack
 Vendor Management System API with Performance Metrics

## Installing and Running

### Database Setup
For database, API is using PostgreSQL. For running the server locally, you'll have to setup PostgreSQL database server.
To install and set up a PostgreSQL database server for your Django project, follow these steps:

**1) Install PostgreSQL:**
  * On Linux:
```sh
sudo apt update
sudo apt install postgresql postgresql-contrib
```
  * On macOS, you can use Homebrew:
```sh
brew install PostgreSQL
```
  * On Windows, download and install the PostgreSQL installer from the official website: https://www.postgresql.org/download/windows/<br>

**2) Start PostgreSQL Service:**
  * On Linux:
```sh
sudo service postgresql start
```
  * On macOS (if installed via Homebrew), PostgreSQL is started automatically after installation.
  * On Windows, PostgreSQL service should start automatically after installation.<br>

**3) Access PostgreSQL Shell:**
  * On Linux:
```sh
sudo -u postgres psql
```
  * On macOS (if installed via Homebrew):
```sh
psql postgres
```
  * On Windows, you can access the PostgreSQL shell from the start menu or use the SQL Shell (psql) installed with PostgreSQL.<br>

**4) Create a New User:**
Once you're in the PostgreSQL shell, run the following command to create a new user (replace 'ventorAdmin' and 'ventorTrack' with your desired username and password):
```sh
CREATE USER ventorAdmin WITH PASSWORD 'ventorTrack';
```
You can also set other properties for the user, such as superuser privileges or specific database access permissions if needed.<br>

**5) Create a Database:**
Still in the PostgreSQL shell, run the following command to create a new database (replace 'VentorTrack' with your desired database name):
```sh
CREATE DATABASE VentorTrack;
```

**6) Grant Permissions to the User:**
After creating the database, grant all privileges on the database to the user:
```sh
GRANT ALL PRIVILEGES ON DATABASE VentorTrack TO ventorAdmin;
```

### API Server Setup
```sh
git clone https://github.com/Kunj-Modi/VendorTrack VendorTrack

cd VendorTrack

python -m venv venv

venv\Scripts\activate

pip install Django djangorestframework

python manage.py migrate

python manage.py runserver
```

## API Endpoints

 * `POST /api/vendors/`: Create a new vendor.<br>
   Fields required:
   * vendor_code: CharField - A unique identifier for the vendor.
   * name: CharField - Vendor's name.
   * contact_details: TextField - Contact information of the vendor.
   * address: TextField - Physical address of the vendor.

 * `GET /api/vendors/`: List all vendors.<br>
   Fields retrieved:
   * vendor_code: CharField - A unique identifier for the vendor.
   * name: CharField - Vendor's name.
   * contact_details: TextField - Contact information of the vendor.
   * address: TextField - Physical address of the vendor.
   * on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
   * quality_rating_avg: FloatField - Average rating of quality based on purchase orders.
   * average_response_time: FloatField - Average time taken to acknowledge purchase orders.
   * fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.

 * `GET /api/vendors/{vendor_id}/`: Retrieve a specific vendor's details.<br>
   Fields retrieved:
   * vendor_code: CharField - A unique identifier for the vendor.
   * name: CharField - Vendor's name.
   * contact_details: TextField - Contact information of the vendor.
   * address: TextField - Physical address of the vendor.
   * on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
   * quality_rating_avg: FloatField - Average rating of quality based on purchase orders.
   * average_response_time: FloatField - Average time taken to acknowledge purchase orders.
   * fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.
  
 * `PUT /api/vendors/{vendor_id}/`: Update a vendor's details.<br>
   Fields required:
   * name: CharField - Vendor's name.
   * contact_details: TextField - Contact information of the vendor.
   * address: TextField - Physical address of the vendor.

 * `DELETE /api/vendors/{vendor_id}/`: Delete a vendor.

 * `POST /api/purchase_orders/`: Create a purchase order.<br>
   Fields required:
   * po_number: CharField - Unique number identifying the PO.
   * vendor: ForeignKey - Link to the Vendor model.
   * order_date: DateTimeField - Date when the order was placed.
   * delivery_date: DateTimeField - Expected or actual delivery date of the order.
   * items: JSONField - Details of items ordered.
   * quantity: IntegerField - Total quantity of items in the PO.
   * issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.

 * `GET /api/purchase_orders/`: List all purchase orders with an option to filter by vendor.<br>
   Fields retrieved:
   * po_number: CharField - Unique number identifying the PO.
   * vendor: ForeignKey - Link to the Vendor model.
   * order_date: DateTimeField - Date when the order was placed.
   * delivery_date: DateTimeField - Expected or actual delivery date of the order.
   * items: JSONField - Details of items ordered.
   * quantity: IntegerField - Total quantity of items in the PO.
   * status: CharField - Current status of the PO (e.g., pending, completed, canceled).
   * quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
   * issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
   * acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.

 * `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.<br>
   Fields retrieved:
   * po_number: CharField - Unique number identifying the PO.
   * vendor: ForeignKey - Link to the Vendor model.
   * order_date: DateTimeField - Date when the order was placed.
   * delivery_date: DateTimeField - Expected or actual delivery date of the order.
   * items: JSONField - Details of items ordered.
   * quantity: IntegerField - Total quantity of items in the PO.
   * status: CharField - Current status of the PO (e.g., pending, completed, canceled).
   * quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
   * issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
   * acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.

 * `PUT /api/purchase_orders/{po_id}/`: Update a purchase order.<br>
   Fields required:
   * vendor: ForeignKey - Link to the Vendor model.
   * order_date: DateTimeField - Date when the order was placed.
   * delivery_date: DateTimeField - Expected or actual delivery date of the order.
   * items: JSONField - Details of items ordered.
   * quantity: IntegerField - Total quantity of items in the PO.
   * status: CharField - Current status of the PO (e.g., pending, completed, canceled).
   * quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
   * issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
   * acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.

 * `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order.

 * `GET /api/vendors/{vendor_id}/performance`: Retrieve a vendor's performance metrics.<br>
   Fields retrieved:
   * vendor: ForeignKey - Link to the Vendor model.
   * date: DateTimeField - Date of the performance record.
   * on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
   * quality_rating_avg: FloatField - Historical record of the quality rating average.
   * average_response_time: FloatField - Historical record of the average response time.
   * fulfillment_rate: FloatField - Historical record of the fulfilment rate.

 * `PUT /api/purchase_orders/{po_number}/acknowledge/`: For vendors to acknowledge POs.<br>
   Fields required:
    * acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.

## Testing

Explore our API endpoints using Postman:
[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.postman.com/lunar-module-architect-59990395/workspace/vendortrack)


## License

This libary is [licensed](LICENSE) under the [MIT Licence](https://en.wikipedia.org/wiki/MIT_License).

