import logging

from src.app import app

def main():
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9000,
        reload=True,
    )

if __name__ == "__main__":
    main()