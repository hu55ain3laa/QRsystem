from sqladmin import Admin, ModelView
from app.models import User, Item
from app.core.db import engine
from fastapi import FastAPI, Depends
from app.core.security import get_password_hash
from sqlmodel import Session
from wtforms import Form, StringField, BooleanField, PasswordField

# Function to get a database session
def get_session():
    with Session(engine) as session:
        yield session

def setup_admin(app: FastAPI) -> None:
    """
    Configure and setup SQLAdmin dashboard
    """
    admin = Admin(app, engine)

    class UserAdmin(ModelView, model=User):
        column_list = ["id", "email", "is_active", "is_superuser", "full_name"]
        column_searchable_list = ["email", "full_name"]
        column_sortable_list = ["email", "is_active", "is_superuser"]
        column_default_sort = [("email", False)]
        
        # Don't show hashed_password in the form
        form_excluded_columns = ["hashed_password"]
        
        # Permissions
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        icon = "fa-solid fa-user"
        name = "User"
        name_plural = "Users"
        
        # Create a custom form with password field
        async def scaffold_form(self, rules=None):
            form = await super().scaffold_form(rules)
            form.password = PasswordField("Password")
            return form
        
        # This hook runs just before saving the model
        async def on_model_change(self, data, model, is_created, request=None):
            # Get password from submitted data
            password_field = "password"
            if password_field in data:
                # Extract the password value
                password = data.pop(password_field)
                if password:
                    # Hash the password and store it in the hashed_password field
                    model.hashed_password = get_password_hash(password)
            # New users must have a password
            elif is_created and not getattr(model, "hashed_password", None):
                raise ValueError("Password is required for new users")

    class ItemAdmin(ModelView, model=Item):
        column_list = ["id", "title", "description", "owner_id"]
        column_searchable_list = ["title", "description"]
        column_sortable_list = ["title"]
        column_default_sort = [("title", False)]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        icon = "fa-solid fa-box"
        name = "Item"
        name_plural = "Items"

    admin.add_view(UserAdmin)
    admin.add_view(ItemAdmin)
    
    return admin 