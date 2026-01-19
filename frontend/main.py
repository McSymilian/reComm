import logging
from src.app import App

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

if __name__ == "__main__":
    app = App()
    app.mainloop()