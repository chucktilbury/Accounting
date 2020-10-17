# These are just random notes that change a lot

## BUGS:
* Prevent saving notes when there is no record to save it to. This currently
  fails silently.
* Can open more than one instance of a dialog. That should not happen. Switch to modal?

## TODO:
* ~~Add a search functionality to the logger dialog.~~
* ~~Organize app into directories to keep the forms and other source separate.~~
* Add some smart to find the database file.
* Add the application state to the database.
  * create a "forms" table where the status of forms is saved.
  * create an "app" table where status of the app is stored.
    * records not saved
    * current customer and vendor
  * restore app and form status when the app is started
* When a sale or purchase is committed, then the accounts are updated.
* Inventory is automatically updated when a sale is made.
* Add progress dialogs for database stuff.
* Add backup/restore for customers and vendors.
* Add reports to menus
* Show balance sheet and P&L on "home" tab
* ~~Add support for a form on a dialog. Differentiate a notebook tab form
  and a dialog form by adding new base classes with overrides.~~
* Decide how to support added logic in a notebook form.
* A customer or vendor cannot be deleted if there are committed
  transactions associated with them.
* If a customer or vendor can be deleted, then also delete uncommitted
  transactions as well.
* A customer or vendor can be modified, as long as committed transactions
  are not disturbed. Committed amounts cannot be altered.
* Associate vendors with accounts. This is used as the default account when
  committing a transaction. The account can be changed when the purchase
  is committed.
* Figure out a way to show uncommitted sales and purchases.
* ~~Figure out a way to avoid duplicating sales and purchases when importing.~~
* Modify product widget so that additional products are selected from a
  non-modal dialog, then displayed in the form.
* Select sales or purchases based on the customer/vendor name. Select dialog
  needs to show if there are uncommitted transactions for that entity.
* Select sales and vendors based on whether they have uncommitted transactions.
* Add better directory and discovery for the SQL init routines.
* Add user land configuration file to the user's home directory.
* Move data directory to userland in home directory.
* ~~Add "search" functionality to C, V, S, and P form browsers.~~
* Add "Actions" to menu.
  * Create C, V, S, or P.
  * Commit S or P.
  * Close books.
  * Spawn the database browser.
* Create the exception classes for the app with logging and dialogs.
* Add validation to the forms.
* ~~Add logic to prompt for a save if the form has been changed.~~
* Devise a way to store the forms in the database.
  * create tables with a form, for the form editor.
  * devise a way to edit the forms with a form editor.
* Add a way to do SQL queries directly. How to use the data generated?

## Reports needed:
* uncommitted sales and purchases
* outstanding sales that are not complete
* balance sheet, etc
* customer sales
* vendor purchases
Move these to menu items with their own dialogs?

## Sales and Purchase Forms
* Need to show the date when the transaction happened.
* When committed is checked, no changes are allowed. If committed is not checked, the
  the edit button is enabled. Otherwise, it's disabled.
* The notes can be edited no matter the committed state. Change edit to edit notes?
* New dialog uses the searchWidget for the name. (need to build selection widget)
* Need a product widget to edit sales.

## Simple Table Widget
This is a simple read-only spreadsheet-like widget. It's used to present lists of
complex objects, such as rows from a database.
* The widget is a form with the same layout as a normal form. It can be added to
  a form using the regular interface. Note that the contents are stored in a
  connector table that ties a sale instance to one or more inventory instances.
* All or part of a database row can be displayed as a row.
* The widget allows adding and deleting rows.
* Rows in the widget are accessed by a displayed line number. Numbering is from '1'.
* The notion of a direct cell and an indirect cell are implented. An indirect cell
  is one where the table has a row ID from another table.
* Column labels are implemented.
* X and Y scroll bars are implemented.
* Cells in the table are based on the tk.Label widget.
* Cells have a small padding around them.
* Cells are placed on an ordinary tk.Frame.
* Rows are a separate widget. The sheet contains the rows.
* The only editing that is allowed is to insert and delete rows. This functionality
  can be diabled.
* All of the cell columns are taken from the same columns in the database.