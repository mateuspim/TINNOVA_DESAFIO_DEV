from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
    dependencies=[],
    responses={403: {"description": "Not enough permissions"}},
)


@router.get("")
async def read_logs(lines: int = 100):
    try:
        with open("app.log", "r") as log_file:
            all_lines = log_file.readlines()
            logs = "".join(all_lines[-lines:])
        return {"logs": logs}
    except FileNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Log file not found")
