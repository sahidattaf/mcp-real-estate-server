from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# ----- Mock Property Data -----
properties = [
    {
        "id": "A302",
        "name": "Oceanview Resort Unit A302",
        "location": "Phuket, Thailand",
        "price": 480000,
        "type": "resort",
        "bedrooms": 3,
        "status": "available"
    },
    {
        "id": "B101",
        "name": "Mountainview Hotel Room B101",
        "location": "Chiang Mai, Thailand",
        "price": 220000,
        "type": "hotel",
        "bedrooms": 2,
        "status": "available"
    }
]

# ----- FastAPI App -----
app = FastAPI()

# ----- Function Schema -----
function_schema = {
    "functions": [
        {
            "name": "list_properties",
            "description": "Lists all available properties.",
            "parameters": {"type": "object", "properties": {}}
        },
        {
            "name": "search_properties",
            "description": "Search properties by location, max price, or type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "max_price": {"type": "number"},
                    "property_type": {"type": "string"}
                }
            }
        }
    ]
}

# ----- API Endpoints -----
@app.get("/functions")
def get_functions():
    return function_schema

class ToolCall(BaseModel):
    function: str
    arguments: Dict[str, Any]

@app.post("/call")
def call_function(call: ToolCall):
    try:
        return handle_tool_call(call.function, call.arguments)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----- Function Handler -----
def handle_tool_call(func: str, args: dict):
    if func == "list_properties":
        return {"properties": properties}

    elif func == "search_properties":
        loc = args.get("location", "").lower()
        max_price = args.get("max_price", float("inf"))
        ptype = args.get("property_type", "").lower()

        results = [
            p for p in properties
            if (loc in p["location"].lower() if loc else True) and
               (p["price"] <= max_price) and
               (ptype in p["type"].lower() if ptype else True)
        ]
        return {"matches": results}

    raise ValueError("Unsupported function")
