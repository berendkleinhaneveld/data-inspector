"""
DataInspector is a simple application for (medical) data inspection. 
Small amount of controls, should be just enough to quickly get a sense
of the data. Uses volume rendering with some simple sliders to control
some predefined transfer functions.

:Authors:
    Berend Klein Haneveld <berendkleinhaneveld@gmail.com>
"""

from PySide.QtCore import Qt
from PySide.QtGui import (QAction, QApplication, QFileDialog, QHBoxLayout,
                          QIcon, QMainWindow, QSizePolicy, QSlider,
                          QVBoxLayout, QWidget)

from core.DataReader import DataReader
from ui.RenderWidget import (RenderTypeCT, RenderTypeMIP, RenderTypeSimple,
                             RenderWidget)


class DataInspector(QMainWindow):
    """
    DataInspector main class
    """

    def __init__(self):
        super(DataInspector, self).__init__()

        self.slider_width = +300

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.render_widget = RenderWidget()

        # Create interface actions
        self.action_load_data = QAction('Load data set', self, shortcut='Ctrl+O')
        self.action_load_data.setIcon(QIcon("images/AddButton.png"))
        self.action_load_data.triggered.connect(self.load_file)
        self.action_show_simple = QAction('Switch to simple rendering', self, shortcut='Ctrl+1')
        self.action_show_simple.setText("Simple")
        self.action_show_simple.triggered.connect(self.switch_to_simple)
        self.action_show_ct = QAction('Switch to CT rendering', self, shortcut='Ctrl+2')
        self.action_show_ct.setText("CT")
        self.action_show_ct.triggered.connect(self.switch_to_ct)
        self.action_show_mip = QAction('Switch to MIP rendering', self, shortcut='Ctrl+3')
        self.action_show_mip.setText("MIP")
        self.action_show_mip.triggered.connect(self.switch_to_mip)

        # Align the dock buttons to the right with a spacer widget
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add buttons to container on top
        self.toolbar = self.addToolBar('Main tools')
        self.toolbar.addAction(self.action_show_simple)
        self.toolbar.addAction(self.action_show_ct)
        self.toolbar.addAction(self.action_show_mip)

        self.toolbar.addWidget(spacer)
        self.toolbar.addAction(self.action_load_data)
        self.setUnifiedTitleAndToolBarOnMac(True)

        # Slider for simple visualization
        self.sliders_simple_widget = QSlider(Qt.Horizontal)
        self.sliders_simple_widget.setMinimumWidth(self.slider_width)
        self.sliders_simple_widget.setMaximumWidth(self.slider_width)
        self.sliders_simple_widget.setMinimum(0)
        self.sliders_simple_widget.setMaximum(1000)
        self.sliders_simple_widget.valueChanged.connect(self.simple_slider_value_changed)
        self.sliders_simple_widget.setHidden(True)

        # Create sliders for CT transfer function
        sliders_layout = QVBoxLayout()
        sliders_layout.setContentsMargins(0, 0, 0, 0)
        sliders_layout.setSpacing(0)
        self.sliders = []
        for _ in range(0, 7):
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(1000)
            slider.valueChanged.connect(self.ct_slider_value_changed)
            self.sliders.append(slider)
            sliders_layout.addWidget(slider)

        self.sliders_ct_widget = QWidget()
        self.sliders_ct_widget.setMinimumWidth(self.slider_width)
        self.sliders_ct_widget.setMaximumWidth(self.slider_width)
        self.sliders_ct_widget.setLayout(sliders_layout)
        self.sliders_ct_widget.setHidden(True)

        self.min_slider = QSlider(Qt.Horizontal)
        self.min_slider.setMinimum(0)
        self.min_slider.setMaximum(1000)
        self.min_slider.valueChanged.connect(self.mip_slider_value_changed)

        self.max_slider = QSlider(Qt.Horizontal)
        self.max_slider.setMinimum(0)
        self.max_slider.setMaximum(1000)
        self.max_slider.setValue(1000)
        self.max_slider.valueChanged.connect(self.mip_slider_value_changed)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.min_slider)
        layout.addWidget(self.max_slider)

        self.sliders_mip_widget = QWidget()
        self.sliders_mip_widget.setMinimumWidth(self.slider_width)
        self.sliders_mip_widget.setMaximumWidth(self.slider_width)
        self.sliders_mip_widget.setLayout(layout)
        self.sliders_mip_widget.setHidden(True)

        layout = QHBoxLayout(self.main_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.render_widget)
        layout.addWidget(self.sliders_mip_widget)
        layout.addWidget(self.sliders_ct_widget)
        layout.addWidget(self.sliders_simple_widget)
        self.main_widget.setLayout(layout)

        self.resize(800, 500)

    def switch_to_simple(self):
        """
        Switch the visualization style to a simple transfer function
        """
        self.render_widget.set_render_type(RenderTypeSimple)

        self.sliders_simple_widget.setDisabled(False)
        self.sliders_ct_widget.setDisabled(True)
        self.sliders_mip_widget.setDisabled(True)

        self.sliders_simple_widget.setHidden(False)
        self.sliders_ct_widget.setHidden(True)
        self.sliders_mip_widget.setHidden(True)

    def switch_to_ct(self):
        """
        Switch to a visualization style that should work pretty ok
        for CT datasets
        """
        self.render_widget.set_render_type(RenderTypeCT)

        self.sliders_simple_widget.setDisabled(True)
        self.sliders_ct_widget.setDisabled(False)
        self.sliders_mip_widget.setDisabled(True)

        self.sliders_simple_widget.setHidden(True)
        self.sliders_ct_widget.setHidden(False)
        self.sliders_mip_widget.setHidden(True)

    def switch_to_mip(self):
        """
        Switch to Maximum intensity projection visualization type
        """
        self.render_widget.set_render_type(RenderTypeMIP)

        self.sliders_simple_widget.setDisabled(True)
        self.sliders_ct_widget.setDisabled(True)
        self.sliders_mip_widget.setDisabled(False)

        self.sliders_simple_widget.setHidden(True)
        self.sliders_ct_widget.setHidden(True)
        self.sliders_mip_widget.setHidden(False)

    def simple_slider_value_changed(self):
        """
        Callback for slider of simple visualization type
        """
        slider_value = float(self.sliders_simple_widget.value()) \
            / float(self.sliders_simple_widget.maximum())
        self.render_widget.lowerBound = self.render_widget.minimum \
            + (self.render_widget.maximum - self.render_widget.minimum) * slider_value
        self.render_widget.update()

    def mip_slider_value_changed(self):
        """
        Callback for sliders of MIP visualization
        """
        min_value = float(self.min_slider.value()) / float(self.min_slider.maximum())
        max_value = float(self.max_slider.value()) / float(self.max_slider.maximum())

        self.render_widget.mipMin = self.render_widget.minimum \
            + (self.render_widget.maximum - self.render_widget.minimum) * min_value
        self.render_widget.mipMax = self.render_widget.minimum \
            + (self.render_widget.maximum - self.render_widget.minimum) * max_value

        self.render_widget.update()

    def ct_slider_value_changed(self):
        """
        Callback for sliders of CT visualization
        """
        for (x, slider) in enumerate(self.sliders):
        # for x in range(0, len(self.sliders)):
            # slider = self.sliders[x]
            slider_value = float(slider.value()) / float(slider.maximum())
            # Use an square function for easier opacity adjustments
            converted_value = slider_value * slider_value * slider_value
            self.render_widget.sectionsOpacity[x] = converted_value

        self.render_widget.update()

    def load_file(self):
        """
        Loads a file from disk
        """
        extensions = DataReader().get_supported_extensions_as_string()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open data set", "",
                                                   "Images (" + extensions + ")")
        if not file_name:
            return

        self.render_widget.load_file(file_name)
        self.switch_to_simple()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    viewer = DataInspector()

    viewer.render_widget.rwi.Start()
    viewer.raise_()
    viewer.show()
    sys.exit(app.exec_())
