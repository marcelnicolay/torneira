from torneira.core.dispatcher import url
from controller.home import HomeController

urls = (
	url(r"/", HomeController, name="home-index"),
)
