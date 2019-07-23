# Item Catalog App

#### create a virtual environment to work on
```
virtualenv venv
source project_path/venv/bin/activate
pip install -r project_path/requirements.txt
```

#### Run the application
```
python3 project_path/run.py
```

1. Show the home page
```
http://localhost:8000/
http://localhost:8000/home
```

2. Registration page
```
http://localhost:8000/register
```

3. Login Page
```
http://localhost:8000/login
```

4. Logout route
```
http://localhost:8000/logout
```

5. Your account page
```
http://localhost:8000/account
```

6. Categories resource
```
# Show all categories
http://localhost:8000/categories

# Add new category
http://localhost:8000/categories/new
```

7. Items resource
```
# Show all items of a specified category
http://localhost:8000/categories/<int:category_id>/items

# Show a particular item of a specified category
http://localhost:8000/categories/<int:category_id>/items/<int:item_id>

# Add an item for a particular category
http://localhost:8000/categories/<int:category_id>/items/new

# Update an item
http://localhost:8000/categories/<int:category_id>/items/<int:item_id>/edit

# Delete an item
http://localhost:8000/categories/<int:category_id>/items/<int:item_id>/delete
```

8. API endpoints
```
# Show all of the categories in a json format
http://localhost:8000/categories/JSON

# Show all of the items in a json format
http://localhost:8000/items/JSON

# Show all of the items of a specific category
http://localhost:8000/categories/<int:category_id>/items/JSON
```
