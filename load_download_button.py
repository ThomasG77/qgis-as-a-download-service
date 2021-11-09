import base64
import urllib.request
from pathlib import Path

from qgis.PyQt.QtWidgets import QAction, QToolBar
from qgis.PyQt.QtGui import (QPixmap, QIcon)
from qgis.utils import iface
from qgis.core import (QgsProject, QgsRasterLayer, Qgis)
import processing


BASE_URL = 'https://step.esa.int/auxdata/dem/SRTMGL1'

def download_nasa_with_credentials(dest, filename):
    url = f"{BASE_URL}/{filename}"
    redirectHandler = urllib.request.HTTPRedirectHandler()
    cookieProcessor = urllib.request.HTTPCookieProcessor()
    passwordManager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passwordManager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
    authHandler = urllib.request.HTTPBasicAuthHandler(passwordManager)
    opener = urllib.request.build_opener(redirectHandler,cookieProcessor,authHandler)
    urllib.request.install_opener(opener)
    return urllib.request.urlretrieve(url, f"{dest}/{filename}")

def download_from_selection():

    project = QgsProject.instance()
    projet_file_name = project.fileName()
    root = project.layerTreeRoot()
    mygroup = root.findGroup("Raster SRTM 30m")
    
    for feat in iface.activeLayer().selectedFeatures():
        raster_path = Path(projet_file_name).parent / 'data' / feat['dataFile']
        file_name = raster_path.stem
        if not raster_path.exists():
            iface.messageBar().pushMessage(f"Downloading {file_name} before adding", level=Qgis.Info, duration=3)
            url = f'{BASE_URL}/{raster_path.name}'
            urllib.request.urlretrieve(url, raster_path)
            # file_size = urllib.request.urlopen(f'https://labs.webgeodatavore.com/partage/SCANEM40K/{raster_path.name}').info().get('Content-Length')
        existing_layers_in_group = [l.name() for l in mygroup.children()]
        if file_name not in existing_layers_in_group:
            raster_layer = QgsRasterLayer(f"/vsizip/{raster_path}/{file_name.split('.')[0]}.hgt", file_name)
            project.addMapLayer(raster_layer, False)
            mygroup.addLayer(raster_layer)
        else:
            iface.messageBar().pushMessage(f"The layer with name {file_name} already present. No need to add", level=Qgis.Info, duration=1)

title = 'Download from selection'

if not iface.mainWindow().findChild(QToolBar,'Download from selection'):
    base64_data = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFXSURBVFiF7dY7SxxRGIfx3+qCFwSxUEihYCGCCEqwcVuDNkoKLQRbQbDxS/gF1Eo7m2AZRO1ECIQQrMTCS5NCVBAJBEQbQYuZ1UF3szO7m1HIPjC3w+H9P8N5OTP872TC6x6GU86ew3o2fGjAZ3xPKXwVWflTyB1uUhK4z9/UpRRYlJpATaAmUBN4c4HoVjyO3pRye/AtKrAVDranJHCC00qLtGEaIxXrlMkAjsOjbN68Cd+lQNM/zKsvJdCIA0xUOTiDRSzHmTyEc8yXmBe3CbNYw090xBGA7rDwkuJ9EkegBTv4iuZCE4oV/4UcPmJDsDRJ+SDY7S4whdskAvAbn/CAbbQmCO/DD2xiVuQvuBzqsYJDdEbGiy1BTvDWM5WEFmIBZxj8i8AkrjBW7fCXAaMFBF4KxuLVxlCCI+zjC64jYV2eP0wnCWuWRT8uBWv9B7uSNekTj5NGO7z2RMCFAAAAAElFTkSuQmCC"

    pm1 = QPixmap()
    pm1.loadFromData(base64.b64decode(base64_data))

    selection_download_action = QAction(
        QIcon(pm1),
        title,
    )
    selection_download_action.triggered.connect(download_from_selection)
    toolbar1 = iface.addToolBar(title)
    toolbar1.setObjectName(title)
    toolbar1.addAction(selection_download_action)
