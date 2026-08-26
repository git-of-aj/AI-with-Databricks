# ======= Sample Data ============
employees = {
    133045: {
        "Name": "Aarav Sharma",
        "Designation": "Software Engineer",
        "Manager Name": "Neha Kapoor",
        "Location": "Noida",
        "Department Name": "Engineering",
        "Leaves availed": 8,
        "Leaves pending": 16
    },
    214672: {
        "Name": "Priya Verma",
        "Designation": "Senior Software Engineer",
        "Manager Name": "Rahul Mehta",
        "Location": "Bengaluru",
        "Department Name": "Engineering",
        "Leaves availed": 11,
        "Leaves pending": 13
    },
    305814: {
        "Name": "Rohan Gupta",
        "Designation": "HR Executive",
        "Manager Name": "Anita Singh",
        "Location": "Gurugram",
        "Department Name": "Human Resources",
        "Leaves availed": 6,
        "Leaves pending": 18
    },
    426931: {
        "Name": "Sneha Iyer",
        "Designation": "Finance Analyst",
        "Manager Name": "Vikram Rao",
        "Location": "Mumbai",
        "Department Name": "Finance",
        "Leaves availed": 9,
        "Leaves pending": 15
    },
    518263: {
        "Name": "Aditya Malhotra",
        "Designation": "Product Manager",
        "Manager Name": "Karan Bhatia",
        "Location": "Pune",
        "Department Name": "Product",
        "Leaves availed": 12,
        "Leaves pending": 12
    },
    609742: {
        "Name": "Kavya Nair",
        "Designation": "UI/UX Designer",
        "Manager Name": "Meera Joshi",
        "Location": "Hyderabad",
        "Department Name": "Design",
        "Leaves availed": 7,
        "Leaves pending": 17
    },
    731056: {
        "Name": "Vivek Choudhary",
        "Designation": "DevOps Engineer",
        "Manager Name": "Sanjay Kumar",
        "Location": "Noida",
        "Department Name": "IT Operations",
        "Leaves availed": 10,
        "Leaves pending": 14
    },
    842319: {
        "Name": "Ananya Singh",
        "Designation": "Business Analyst",
        "Manager Name": "Rajiv Sharma",
        "Location": "Delhi",
        "Department Name": "Business Operations",
        "Leaves availed": 5,
        "Leaves pending": 19
    },
    953684: {
        "Name": "Arjun Patel",
        "Designation": "Sales Executive",
        "Manager Name": "Pooja Agarwal",
        "Location": "Ahmedabad",
        "Department Name": "Sales",
        "Leaves availed": 13,
        "Leaves pending": 11
    },
    164527: {
        "Name": "Ishita Mehta",
        "Designation": "Marketing Specialist",
        "Manager Name": "Nitin Khanna",
        "Location": "Mumbai",
        "Department Name": "Marketing",
        "Leaves availed": 8,
        "Leaves pending": 16
    },
    275841: {
        "Name": "Manish Tiwari",
        "Designation": "QA Engineer",
        "Manager Name": "Deepak Sinha",
        "Location": "Bengaluru",
        "Department Name": "Quality Assurance",
        "Leaves availed": 14,
        "Leaves pending": 10
    },
    386295: {
        "Name": "Simran Kaur",
        "Designation": "Recruiter",
        "Manager Name": "Ritu Sharma",
        "Location": "Gurugram",
        "Department Name": "Human Resources",
        "Leaves availed": 4,
        "Leaves pending": 20
    },
    497613: {
        "Name": "Yash Agarwal",
        "Designation": "Data Analyst",
        "Manager Name": "Amit Verma",
        "Location": "Hyderabad",
        "Department Name": "Data & Analytics",
        "Leaves availed": 9,
        "Leaves pending": 15
    },
    528704: {
        "Name": "Pallavi Deshmukh",
        "Designation": "Project Manager",
        "Manager Name": "Suresh Iyer",
        "Location": "Pune",
        "Department Name": "Project Management",
        "Leaves availed": 15,
        "Leaves pending": 9
    },
    639182: {
        "Name": "Kunal Saxena",
        "Designation": "Backend Developer",
        "Manager Name": "Neha Kapoor",
        "Location": "Noida",
        "Department Name": "Engineering",
        "Leaves availed": 6,
        "Leaves pending": 18
    },
    740526: {
        "Name": "Riya Kapoor",
        "Designation": "Content Writer",
        "Manager Name": "Alok Mehta",
        "Location": "Delhi",
        "Department Name": "Content",
        "Leaves availed": 10,
        "Leaves pending": 14
    },
    851437: {
        "Name": "Siddharth Jain",
        "Designation": "System Administrator",
        "Manager Name": "Vikram Rao",
        "Location": "Mumbai",
        "Department Name": "IT Operations",
        "Leaves availed": 7,
        "Leaves pending": 17
    },
    962815: {
        "Name": "Neelam Joshi",
        "Designation": "Finance Manager",
        "Manager Name": "Sunil Gupta",
        "Location": "Kolkata",
        "Department Name": "Finance",
        "Leaves availed": 12,
        "Leaves pending": 12
    },
    173604: {
        "Name": "Varun Bansal",
        "Designation": "Customer Support Executive",
        "Manager Name": "Shweta Arora",
        "Location": "Chandigarh",
        "Department Name": "Customer Support",
        "Leaves availed": 5,
        "Leaves pending": 19
    },
    284759: {
        "Name": "Megha Reddy",
        "Designation": "Product Designer",
        "Manager Name": "Meera Joshi",
        "Location": "Hyderabad",
        "Department Name": "Design",
        "Leaves availed": 11,
        "Leaves pending": 13
    }
}

# 24 leaves allocated per employee per year
TOTAL_LEAVES = 24

# ====================== MCP Server Code =================

from fastmcp import FastMCP

mcp = FastMCP("Leave Balance checker")

@mcp.tool
def check_employee_details(empID: int) -> dict:
    """
    Read complete details of an employee.

    Args:
        empID: Six-digit employee ID.

    Returns:
        Complete employee details including leave balance.
    """

    if empID not in employees:
        return {
            "success": False,
            "message": f"Employee ID {empID} not found."
        }

    return {
        "success": True,
        "employee_id": empID,
        "employee": employees[empID]
    }


@mcp.tool
def update_employee_details(
    empID: int,
    name: str = None,
    designation: str = None,
    manager_name: str = None,
    location: str = None,
    department_name: str = None,
    leaves_availed: int = None
) -> dict:
    """
    Update employee details.

    Only the fields provided by the caller will be updated.
    Leaves pending is automatically recalculated from 24 annual leaves.

    Args:
        empID: Six-digit employee ID.
        name: Employee's name.
        designation: Employee's designation.
        manager_name: Employee's manager.
        location: Employee's location.
        department_name: Employee's department.
        leaves_availed: Number of leaves already availed.

    Returns:
        Updated employee details.
    """

    if empID not in employees:
        return {
            "success": False,
            "message": f"Employee ID {empID} not found."
        }

    employee = employees[empID]

    # Update only fields that were provided
    if name is not None:
        employee["Name"] = name

    if designation is not None:
        employee["Designation"] = designation

    if manager_name is not None:
        employee["Manager Name"] = manager_name

    if location is not None:
        employee["Location"] = location

    if department_name is not None:
        employee["Department Name"] = department_name

    if leaves_availed is not None:

        if leaves_availed < 0 or leaves_availed > TOTAL_LEAVES:
            return {
                "success": False,
                "message": f"Leaves availed must be between 0 and {TOTAL_LEAVES}."
            }

        employee["Leaves availed"] = leaves_availed
        employee["Leaves pending"] = TOTAL_LEAVES - leaves_availed

    return {
        "success": True,
        "message": f"Employee {empID} updated successfully.",
        "employee_id": empID,
        "employee": employee
    }

