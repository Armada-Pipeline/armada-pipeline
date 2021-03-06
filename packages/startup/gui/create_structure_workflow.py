﻿"""
Startup main window
"""
from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource

import utilsa

logging = utilsa.Logger('armada')


class CreateStructureWorkflow(QtWidgets.QWidget):
	"""Sets up user and/or shared data depending on type of setup process
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"
	nextPressed = QtCore.Signal()

	def __init__(self, parent=None):
		"""
		Args:
			flow: What part of setup is the user entering into?
		"""
		super(CreateStructureWorkflow, self).__init__(parent)

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Workplace creation starting...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.parent = parent
		self.armada_root_path = definitions.ROOT_PATH

		# self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.sizeHint()

		# GUI ----------------------------------
		self.btn_back = QtWidgets.QPushButton()
		self.btn_back.setIcon(resource.color_svg('arrow_left', 128, '#9E9E9E'))
		self.btn_back.setIconSize(QtCore.QSize(30, 30))
		self.btn_back.setFixedHeight(30)
		self.btn_back.setStyleSheet(resource.style_sheet('push_button_w_icon'))

		self.tb_welcome = QtWidgets.QLabel()
		self.tb_welcome.setText("""
			<p style="font-size:30px;font-weight: normal;">How should we organize this project?</p>"""
		)
		self.tb_welcome.setWordWrap(True)

		self.tb_description = QtWidgets.QLabel()
		self.tb_description.setStyleSheet("""
			background-color: transparent;
			font: 12px;
			font-weight: normal"""
		)
		self.tb_description.setText("""
			<p>Each project utilizes a set of rules called a <b>structure</b> to enforce folder/file locations and naming conventions.
			<p>Once configured a structure automatically makes sure everyone adheres to the ruleset so you can focus on what you do best: Makin art!</p>"""
		)
		self.tb_description.setWordWrap(True)

		# Input
		self.lbl_structure_workflow = QtWidgets.QLabel("Choose a structure workflow")

		self.lw_items = QtWidgets.QListWidget()
		self.lw_items.setViewMode(QtWidgets.QListView.IconMode)
		# self.lw_items.setMaximumHeight(50)
		# self.lw_items.setResizeMode(QtWidgets.QListView.Fixed)
		self.lw_items.setUniformItemSizes(True)
		self.lw_items.setSizeAdjustPolicy(QtWidgets.QListWidget.AdjustIgnored)
		self.lw_items.setMovement(self.lw_items.Static)
		self.lw_items.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents);
		self.lw_items.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);
		self.lw_items.setFlow(QtWidgets.QListView.LeftToRight)
		# self.lw_items.setSpacing(5)
		self.lw_items.setMinimumHeight(100)
		self.lw_items.setStyleSheet("""
				QListView{
					show-decoration-selected: 0;
					background: #262626;
					color:rgb(218,218,218) ;
					font:12px "Roboto-Thin";
					border: none;
					height: 200px;
					outline: 0;
					padding-left: 10;
					padding-right: 10;
				}
				""")

		# Structure workflow options
		builtin_icon = resource.color_svg('folder_folder', 1024, '#F9D085')
		lw_item = QtWidgets.QListWidgetItem(builtin_icon, 'Built In Structure')
		lw_item.setSizeHint(self.lw_items.sizeHint())
		self.lw_items.addItem(lw_item)

		custom_icon = resource.color_svg('structure_create', 1024, '#7D7D7D')
		lw_item = QtWidgets.QListWidgetItem(custom_icon, 'Custom Structure')
		lw_item.setSizeHint(self.lw_items.sizeHint())
		# lw_item.setFlags(QtCore.Qt.ItemIsSelectable)  # TODO: enable when custom structures workflow is figured out
		self.lw_items.addItem(lw_item)

		self.lbl_structure_description = QtWidgets.QLabel()
		self.lbl_structure_description.setWordWrap(True)
		self.lbl_structure_description.setStyleSheet("""
			background-color: transparent;
			font: 12px;
			font-weight: normal"""
		)

		self.hline_username = QtWidgets.QFrame()
		self.hline_username.setFixedHeight(1)
		self.hline_username.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_username.setStyleSheet("background-color: #636363;")

		self.btn_next = QtWidgets.QPushButton('Next')
		self.btn_next.setFixedWidth(100)
		self.btn_next.setStyleSheet('''
			QPushButton{
				Background:#2e7a78;
				height: 30px;
				font: 12px "Roboto-Thin"
			}
			QPushButton:hover{
				Background: #369593;
			}
			QPushButton:hover:pressed{
				Background: #2e7a78;
			}
			QPushButton:pressed{
				Background:  #2a615f;
			}
			QPushButton:disabled{
				Background: #3b3b3b;
			}'''
		)
		self.btn_next.setFixedSize(100, 40)
		self.btn_next.setEnabled(False)

		# self.lbl_disclaimer = QtWidgets.QTextBrowser()
		# self.lbl_disclaimer.setReadOnly(True)
		# self.lbl_disclaimer.setText('Armada Pipeline does not store passwords or account data at this time. Your acocunt is stored locally and only used to add another degree of flexibility project')
		# self.lbl_disclaimer.setMinimumSize(100, 50)

		# Layout --------------------------------------------
		btn_back_layout = QtWidgets.QVBoxLayout()
		btn_back_layout.addWidget(self.btn_back)
		btn_back_layout.setAlignment(QtCore.Qt.AlignTop)
		btn_back_layout.setContentsMargins(0, 0, 0, 0)
		btn_back_layout.setSpacing(0)

		description_layout = QtWidgets.QVBoxLayout()
		description_layout.addWidget(self.tb_welcome)
		description_layout.addWidget(self.tb_description)
		description_layout.setAlignment(QtCore.Qt.AlignTop)
		description_layout.setContentsMargins(0, 0, 0, 0)
		description_layout.setSpacing(30)

		input_layout = QtWidgets.QVBoxLayout()
		input_layout.addWidget(self.lbl_structure_workflow)
		input_layout.addWidget(self.lw_items)
		input_layout.addWidget(self.lbl_structure_description)
		input_layout.setAlignment(QtCore.Qt.AlignTop)
		input_layout.setContentsMargins(0, 0, 0, 0)
		input_layout.setSpacing(10)

		btn_layout = QtWidgets.QVBoxLayout()
		btn_layout.addWidget(self.btn_next)
		btn_layout.setAlignment(QtCore.Qt.AlignTop)
		btn_layout.setContentsMargins(0, 0, 0, 0)
		btn_layout.setSpacing(0)

		contents_layout = QtWidgets.QVBoxLayout()
		contents_layout.addLayout(description_layout)
		contents_layout.addLayout(input_layout)
		contents_layout.addLayout(btn_layout)
		contents_layout.addStretch()
		contents_layout.setAlignment(QtCore.Qt.AlignTop)
		contents_layout.setContentsMargins(0, 0, 0, 0)
		contents_layout.setSpacing(50)

		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addLayout(btn_back_layout)
		self.main_layout.addLayout(contents_layout)
		self.main_layout.setContentsMargins(20, 20, 60, 20)
		self.main_layout.setSpacing(10)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		# self.btn_next.clicked.connect(self._on_next)
		self.lw_items.itemClicked.connect(self._lw_sel_changed)

	def _lw_sel_changed(self, index):
		# Structure setup
		if index.data(QtCore.Qt.DisplayRole) == "Built In Structure":
			self.lbl_structure_description.setText("""
			<p><b>Built in structures:</b></p>
			<li>- Game Development</li> 
			<li>- Film Production</li>
			<p><b>[NOTE]</b> Structures cannot be changed at this time without destroying the project's data. To 
			try a different structure please create another project.</p>""")
			self.btn_next.setDisabled(False)

		elif index.data(QtCore.Qt.DisplayRole) == "Custom Structure":
			self.lbl_structure_description.setText("""[IN DEVELOPMENT] Create your own <b>custom structure</b>.""")
			self.btn_next.setDisabled(True)



	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			if self.btn_next.isEnabled():
				self.btn_next.clicked.emit()
				return True
			else:
				return False
		if event.key() == QtCore.Qt.Key_Escape:
			return False
		else:
			super(CreateStructureWorkflow, self).keyPressEvent(event)