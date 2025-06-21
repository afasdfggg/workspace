from app.schemas.admin import Admin, AdminCreate, AdminUpdate, AdminWithApiKey
from app.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate, EmployeeSetPassword, EmployeeLogin
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.schemas.time_tracking import Shift, ShiftCreate, ShiftUpdate, ProjectTime
from app.schemas.screenshot import Screenshot, ScreenshotCreate, ScreenshotResponse
from app.schemas.token import Token, TokenPayload