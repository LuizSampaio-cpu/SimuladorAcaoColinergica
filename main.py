import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QCheckBox, QFileDialog)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QPalette, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from matplotlib.animation import FuncAnimation


class HeartbeatAnimation(QLabel):
    def __init__(self):
        super().__init__()
        self.systole_image = QPixmap("assets/Sístole.jpg")
        self.diastole_image = QPixmap("assets/Diástole.jpg")
        self.current_image = self.systole_image
        self.setFixedSize(400, 400)
        self.setScaledContents(True)
        self.setPixmap(self.current_image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(700)  # Intervalo inicial padrão de 500ms

    def update_image(self):
        if self.current_image == self.systole_image:
            self.current_image = self.diastole_image
        else:
            self.current_image = self.systole_image
        self.setPixmap(self.current_image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def set_speed(self, interval):
        self.timer.setInterval(interval)

class HeartRateGraph(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        super().__init__(self.fig)

        self.ax.set_ylim(0, 200)
        self.ax.set_xlim(0, 10)
        self.ax.set_xlabel('')
        self.ax.set_ylabel('Pressão Arterial', fontsize=22)
        self.ax.set_title('Efeito da Droga na Pressão Arterial', fontsize=22)
        self.ax.tick_params(axis='both', labelsize=22)
        self.line, = self.ax.plot([], [], lw=2)
        self.anim = None


    def apply_drug(self, drug_name):
        self.x = np.linspace(0, 10, 100)
        
        if drug_name == "Noradrenalina 20mcg":
            self.y = self.effect_noradrenalina(self.x)
        elif drug_name == "Adrenalina 20mcg":
            self.y = self.effect_adrenalina(self.x)
        elif drug_name == "Isoprenalina 20mcg":
            self.y = self.effect_isoprenalina(self.x)
        elif drug_name == "Efedrina 5mg":
            self.y = self.effect_efedrina(self.x)
        elif drug_name == "Acetilcolina 20mcg":
            self.y = self.effect_acetilcolina(self.x)
        elif drug_name == "Pilocarpina 1,5mg":
            self.y = self.effect_pilocarpina(self.x)
        elif drug_name == "Alfabloqueador":
            self.y = self.effect_alfabloqueador(self.x)
        elif drug_name == "Neostigmina 0,5mg":
            self.y = self.effect_neostigmina(self.x)
        elif drug_name == "Nicotina 300mg":
            self.y = self.effect_nicotina(self.x)
        elif drug_name == "Propanolol 10mg":
            self.y = self.effect_propanolol(self.x)
        elif drug_name == "Atropina 10mg":
            self.y = self.effect_atropina(self.x)
        elif drug_name == "Hexametonio 20mg":
            self.y = self.effect_hexametonio(self.x)
        else:
            self.y = np.full_like(self.x, 120)

        
            
        self.line.set_data([], [])
        self.ax.relim()
        self.ax.autoscale_view()
        self.anim = FuncAnimation(self.fig, self.update_graph, frames=len(self.x), interval=100, blit=False, repeat=False)
        self.anim._stop = self.on_animation_complete
        self.draw()

    def update_graph(self, i):
        self.line.set_data(self.x[:i], self.y[:i])
        return self.line,

    def on_animation_complete(self):
        self.save_graph()

    def save_graph(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Gráfico", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_path:
            # Obtém o nome da droga administrada
            if self.parent() and hasattr(self.parent(), 'current_drug'):
                drug_name = self.parent().current_drug
            else:
                drug_name = "Droga não especificada"

            original_title = self.ax.get_title()
            self.ax.set_title(f"Efeito da Droga: {drug_name}")

            self.line.set_data(self.x, self.y)
            self.ax.relim()
            self.ax.autoscale_view()
            self.draw()
            self.fig.savefig(file_path, format="pdf", bbox_inches="tight")

            # Restaura o título original após salvar
            self.ax.set_title(original_title)

           


    def effect_noradrenalina(self, x):
        y_initial = 120
        slope_up = 15
        slope_down = -15
        y = np.piecewise(x, 
                         [x < 3, (x >= 3) & (x < 5), (x >= 5) & (x < 7), x >= 7], 
                         [y_initial, 
                          lambda x: slope_up * (x - 3) + y_initial,  
                          lambda x: slope_down * (x - 5) + (slope_up * 2) + y_initial,  
                          y_initial])  
        return y

    def effect_adrenalina(self, x):
        y_initial = 120
        max_pressure = 150
        min_pressure = 110
        slope_up = (max_pressure - y_initial) / 2
        slope_down = (min_pressure - max_pressure) / 2
        slope_up_final = (y_initial - min_pressure) / 2

        y = np.piecewise(
            x,
            [x < 3, (x >= 3) & (x < 5), (x >= 5) & (x < 7), (x >= 7) & (x < 9), x >= 9],
            [
                y_initial, 
                lambda x: slope_up * (x - 3) + y_initial, 
                lambda x: slope_down * (x - 5) + max_pressure,
                lambda x: slope_up_final * (x - 7) + min_pressure, 
                y_initial 
            ]
        )
        return y
    
    def effect_isoprenalina(self, x):
        y_initial = 120
        min_pressure = 60 
        slope_down = (min_pressure - y_initial) / 0.5 
        slope_up = (y_initial - min_pressure) / 0.5 

        y = np.piecewise(
            x,
            [
                x < 3,
                (x >= 3) & (x < 3.5), 
                (x >= 3.5) & (x < 4), 
                x >= 4, 
            ],
            [
                y_initial, 
                lambda x: slope_down * (x - 3) + y_initial, 
                lambda x: slope_up * (x - 3.5) + min_pressure, 
                y_initial, 
            ]
        )
        return y

    
    def effect_efedrina(self, x):
        y_initial = 120 
        max_pressure = 140 
        slope_up = (max_pressure - y_initial) / 2  
        slope_down = (y_initial - max_pressure) / 2  

        y = np.piecewise(
            x,
            [x < 3, (x >= 3) & (x < 5), (x >= 5) & (x < 8), (x >= 8) & (x < 10), x >= 10],
            [
                y_initial,  
                lambda x: slope_up * (x - 3) + y_initial,  
                max_pressure, 
                lambda x: slope_down * (x - 8) + max_pressure,  
                y_initial  
            ]
        )
        return y
    
    def effect_acetilcolina(self, x):
        y_initial = 120
        min_pressure = 90  
        slope_down = (min_pressure - y_initial) 
        slope_up = (y_initial - min_pressure)  

        y = np.piecewise(
            x,
            [x < 2, (x >= 2) & (x < 3), (x >= 3) & (x < 4), x >= 4],
            [
                y_initial,  
                lambda x: slope_down * (x - 2) + y_initial,  
                lambda x: slope_up * (x - 3) + min_pressure,  
                y_initial  
            ]
        )
        return y
    
    def effect_pilocarpina(self, x):
        y_initial = 120
        min_pressure = 80  
        slope_down = (min_pressure - y_initial) / 0.5 
        slope_up = (y_initial - min_pressure) / 2  

        y = np.piecewise(
            x,
            [x < 2, (x >= 2) & (x < 2.5), (x >= 2.5) & (x < 3.5), (x >= 3.5) & (x < 5.5), x >= 5.5],
            [
                y_initial, 
                lambda x: slope_down * (x - 2) + y_initial,  
                min_pressure,  
                lambda x: slope_up * (x - 3.5) + min_pressure,  
                y_initial  
            ]
        )
        return y
    
    def effect_alfabloqueador(self, x):
        y_initial = 120
        y_stabilize_low = 100 
        max_pressure = 130  
        min_pressure = 80 
        y = np.piecewise(
            x,
            [ x < 2, (x >= 2) & (x < 3), (x >= 3) & (x < 4), (x >= 4) & (x < 4.5), (x >= 4.5) & (x < 5), (x >= 5) & (x < 6), x >= 6,],
            [
                y_initial,  
                lambda x: (y_stabilize_low - y_initial) * (x - 2) / 1 + y_initial,  
                y_stabilize_low,  
                lambda x: (max_pressure - y_stabilize_low) * (x - 4) / 0.5 + y_stabilize_low, 
                max_pressure, 
                lambda x: (min_pressure - max_pressure) * (x - 5) / 1 + max_pressure,  
                y_initial, 
            ]
        )
        return y
    
    def effect_neostigmina(self, x):
        y_initial = 120  
        y_mid = 110  
        y_low = 60  
        y = np.piecewise(
            x,
            [  x < 1, (x >= 1) & (x < 1.4), (x >= 1.4) & (x < 2.4), (x >= 2.4) & (x < 3.4), (x >= 3.4) & (x < 3.8), (x >= 3.8) & (x < 5.8), x >= 5.8,],
            [
                y_initial,  
                lambda x: (y_mid - y_initial) * (x - 1) / 0.4 + y_initial, 
                y_mid,  
                lambda x: (y_low - y_mid) * (x - 2.4) / 1 + y_mid, 
                y_low,  
                lambda x: (y_initial - y_low) * (x - 3.8) / 2 + y_low,  
                y_initial, 
            ]
        )
        return y
    
    def effect_nicotina(self, x):
        y_initial = 120
        y_mid1 = 110
        y_high = 140
        y_mid2 = 130

        y = np.piecewise(
            x,
            [ x < 1, (x >= 1) & (x < 1.8), (x >= 1.8) & (x < 2.6), (x >= 2.6) & (x < 3.4), (x >= 3.4) & (x < 4.2), (x >= 4.2) & (x < 5), 
             (x >= 5) & (x < 5.8), (x >= 5.8) & (x < 6.6),  x >= 6.6, ],
            [
                y_initial,
                lambda x: (y_mid1 - y_initial) * (x - 1) / 0.8 + y_initial,
                y_mid1,
                lambda x: (y_high - y_mid1) * (x - 2.6) / 0.8 + y_mid1,
                lambda x: (y_mid2 - y_high) * (x - 3.4) / 0.8 + y_high,
                y_mid2,  
                lambda x: (y_high - y_mid2) * (x - 5) / 0.8 + y_mid2,  
                lambda x: (y_initial - y_high) * (x - 5.8) / 0.8 + y_high,  
                y_initial, 
            ]
        )
        return y
    
    def effect_propanolol(self, x):
        y_initial = 120
        y_high = 140

        y = np.piecewise(
            x,
            [
                x < 3,  
                (x >= 3) & (x < 4),  
                (x >= 4) & (x < 5),
                (x >= 5) & (x < 6),  
                (x >= 6) & (x < 7),  
                (x >= 7) & (x < 8),  
                x >= 8,  
            ],
            [
                y_initial,  
                lambda x: (y_high - y_initial) * (x - 3) / 1 + y_initial, 
                lambda x: (y_initial - y_high) * (x - 4) /1 + y_high,
                y_initial, 
                lambda x: (y_high - y_initial) * (x - 6) /1 + y_initial,
                lambda x: (y_initial - y_high) * (x - 7) / 1 + y_high,  
                y_initial, 
            ]
        )
        return y
    
    def effect_atropina(self, x):
        y_initial = 120
        y_high = 150
        y_mid = 140

        y = np.piecewise(
            x,
            [
                x < 3,  
                (x >= 3) & (x < 4),  
                (x >= 4) & (x < 4.5), 
                (x >= 4.5) & (x < 5), 
                (x >= 5) & (x < 6),  
                x >= 6,  
            ],
            [
                y_initial,  
                lambda x: (y_high - y_initial) * (x - 3) / 1 + y_initial,  
                lambda x: (y_mid - y_high) * (x - 4) / 0.5 + y_high,  
                lambda x: (y_high - y_mid) * (x - 4.5) / 0.5 + y_mid,  
                lambda x: (y_initial - y_high) * (x - 5) / 1 + y_high,  
                y_initial,  
            ]
        )
        return y
    
    def effect_hexametonio(self, x):
        y_initial = 120
        y_low = 110

        y = np.piecewise(
            x,
            [
                x < 3,  
                (x >= 3) & (x < 3.5),  
                x >= 3.5,  
            ],
            [
                y_initial,  
                lambda x: (y_low - y_initial) * (x - 3) / 0.5 + y_initial,  
                y_low,  
            ]
        )
        return y




class HeartSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simulador de Atividade Cardíaca')

        self.central_widget = QWidget()
        self.central_widget.setAutoFillBackground(True)
        palette = self.central_widget.palette()
        palette.setColor(QPalette.Window, QColor(Qt.white))
        self.central_widget.setPalette(palette)
        self.setCentralWidget(self.central_widget)

        self.heartbeat_animation = HeartbeatAnimation()
        self.heart_rate_graph = HeartRateGraph()

        self.legend_label = QLabel("Legenda: Nenhuma droga aplicada.")
        self.legend_label.setAlignment(Qt.AlignCenter)
        self.legend_label.setStyleSheet("font-size: 20px; color: black;")

        self.select_label = QLabel("Selecione uma droga para analisar (doses para um cão de 10kg)")
        self.select_label.setAlignment(Qt.AlignCenter)
        self.select_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")

        self.drug_checkboxes = {}
        drug_names = [
            "Noradrenalina 20mcg", "Alfabloqueador", "Neostigmina 0,5mg", 
            "Adrenalina 20mcg", "Propanolol 10mg", "Pilocarpina 1,5mg", 
            "Isoprenalina 20mcg", "Acetilcolina 20mcg", "Nicotina 300mg", 
            "Efedrina 5mg", "Atropina 10mg", "Hexametonio 20mg", "Nenhuma"
        ]

        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.graph_layout = QVBoxLayout()
        self.graph_layout.setSpacing(2)
        self.grid_layout = QGridLayout()

        self.top_layout.addWidget(self.heartbeat_animation)
        self.graph_layout.addWidget(self.heart_rate_graph)
        self.graph_layout.addWidget(self.legend_label)
        self.top_layout.addLayout(self.graph_layout)

        for i, drug in enumerate(drug_names):
            checkbox = QCheckBox(drug)
            checkbox.setStyleSheet("font-size: 24px; padding: 8px;")
            self.drug_checkboxes[drug] = checkbox
            self.grid_layout.addWidget(checkbox, i // 3, i % 3)
        
        self.drug_checkboxes["Alfabloqueador"].stateChanged.connect(self.handle_alfabloqueador_selection)
        self.drug_checkboxes["Neostigmina 0,5mg"].stateChanged.connect(self.handle_neostigmina_selection)
        self.drug_checkboxes["Propanolol 10mg"].stateChanged.connect(self.handle_propanolol_selection)
        self.drug_checkboxes["Atropina 10mg"].stateChanged.connect(self.handle_atropina_selection)
        self.drug_checkboxes["Hexametonio 20mg"].stateChanged.connect(self.handle_hexametonio_selection)


        self.next_button = QPushButton('Aplicar')
        self.next_button.clicked.connect(self.apply_selected_drugs)
        self.save_button = QPushButton('Salvar')
        self.save_button.clicked.connect(self.save_graph_to_pdf)
        self.close_button = QPushButton('Fechar')
        self.close_button.clicked.connect(self.close)
        self.next_button.setStyleSheet("font-size: 24px; padding: 10px;")
        self.save_button.setStyleSheet("font-size: 24px; padding: 10px;")
        self.close_button.setStyleSheet("font-size: 24px; padding: 10px;")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)
        self.grid_layout.addLayout(button_layout, len(drug_names) // 3 + 1, 0, 1, 3)

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.select_label)
        self.main_layout.addLayout(self.grid_layout)

        self.central_widget.setLayout(self.main_layout)

    def handle_alfabloqueador_selection(self, state):
        if state == Qt.Checked:
            self.drug_checkboxes["Adrenalina 20mcg"].setChecked(True)
            self.drug_checkboxes["Noradrenalina 20mcg"].setChecked(True)
        elif state == Qt.Unchecked:
            self.drug_checkboxes["Adrenalina 20mcg"].setChecked(False)
            self.drug_checkboxes["Noradrenalina 20mcg"].setChecked(False)
    
    def handle_neostigmina_selection(self, state):
        if state == Qt.Checked:
            self.drug_checkboxes["Acetilcolina 20mcg"].setChecked(True)
        elif state == Qt.Unchecked:
            self.drug_checkboxes["Acetilcolina 20mcg"].setChecked(False)
    
    def handle_propanolol_selection(self, state):
        if state == Qt.Checked:
            self.drug_checkboxes["Noradrenalina 20mcg"].setChecked(True)
            self.drug_checkboxes["Isoprenalina 20mcg"].setChecked(True)
            self.drug_checkboxes["Adrenalina 20mcg"].setChecked(True)
        elif state == Qt.Unchecked:
            self.drug_checkboxes["Noradrenalina 20mcg"].setChecked(False)
            self.drug_checkboxes["Isoprenalina 20mcg"].setChecked(False)
            self.drug_checkboxes["Adrenalina 20mcg"].setChecked(False)

    def handle_atropina_selection(self, state):
        if state == Qt.Checked:
            self.drug_checkboxes["Acetilcolina 20mcg"].setChecked(True)
            self.drug_checkboxes["Pilocarpina 1,5mg"].setChecked(True)
        elif state == Qt.Unchecked:
            self.drug_checkboxes["Acetilcolina 20mcg"].setChecked(False)
            self.drug_checkboxes["Pilocarpina 1,5mg"].setChecked(False)
    
    def handle_hexametonio_selection(self, state):
        if state == Qt.Checked:
            self.drug_checkboxes["Nicotina 300mg"].setChecked(True)
            self.drug_checkboxes["Atropina 10mg"].setChecked(True)
        elif state == Qt.Unchecked:
            self.drug_checkboxes["Nicotina 300mg"].setChecked(False)
            self.drug_checkboxes["Atropina 10mg"].setChecked(False)


    def apply_selected_drugs(self):
        
        selected_drugs = [drug for drug, checkbox in self.drug_checkboxes.items() if checkbox.isChecked()]
        
        self.current_drug = selected_drugs[0] if selected_drugs else "Nenhuma droga aplicada"

        if "Noradrenalina 20mcg" in selected_drugs:
            self.apply_noradrenalina_effect()
        if "Adrenalina 20mcg" in selected_drugs:
            self.apply_adrenalina_effect()
        if "Isoprenalina 20mcg" in selected_drugs:
            self.apply_isoprenalina_effect()
        if "Efedrina 5mg" in selected_drugs:
            self.apply_efedrina_effect()
        if "Acetilcolina 20mcg" in selected_drugs:
            self.apply_acetilcolina_effect()
        if "Pilocarpina 1,5mg" in selected_drugs:
            self.apply_pilocarpina_effect()
        if "Alfabloqueador" in selected_drugs:
            self.apply_alfabloqueador_effect()
            self.handle_alfabloqueador_selection(True)
        if "Neostigmina 0,5mg" in selected_drugs:
            self.apply_neostigmina_effect()
            self.handle_neostigmina_selection(True)
        if "Nicotina 300mg" in selected_drugs:
            self.apply_nicotina_effect()
        if "Propanolol 10mg" in selected_drugs:
            self.apply_propanolol_effect()
        if "Atropina 10mg" in selected_drugs:
            self.apply_atropina_effect()
        if "Hexametonio 20mg" in selected_drugs:
            self.apply_hexametonio_effect()



    def save_graph_to_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Gráfico como PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        
        if file_path:
            from matplotlib.backends.backend_pdf import PdfPages
            # Criar um PDF e salvar a figura completa
            with PdfPages(file_path) as pdf:
                figure = self.heart_rate_graph.figure  # Acessa a figura completa do gráfico
                figure.savefig(pdf, format='pdf')

        
    def apply_noradrenalina_effect(self):
        self.heart_rate_graph.apply_drug("Noradrenalina 20mcg")
        self.legend_label.setText("<b>Noradrenalina:</b> Estímulo dos receptores alfa1 e beta1. Provoca vasoconstrição, que eleva a pressão arterial.<br>Estímulo do beta1 provoca taquicardia e aumenta a pressão sanguínea. <br>Devido ao grande aumento da PA, ocorrem reflexos que vencem o estímulo beta, provocando bradicardia reflexa.")
        self.heartbeat_animation.set_speed(700)
        QTimer.singleShot(3000, lambda: self.heartbeat_animation.set_speed(200))
        QTimer.singleShot(6000, lambda: self.heartbeat_animation.set_speed(700))
        QTimer.singleShot(9000, lambda: self.heartbeat_animation.set_speed(500))

    def apply_adrenalina_effect(self):
        self.heart_rate_graph.apply_drug("Adrenalina 20mcg")
        self.legend_label.setText("<b>Adrenalina:</b> Estímulo dos receptores alfa1, gerando vasoconstrição, beta1 provocando taquicardia e beta2, provocando vasodilatação na área dos músculos. <br>Elevação da PA.")
        self.heartbeat_animation.set_speed(700)
        QTimer.singleShot(3000, lambda: self.heartbeat_animation.set_speed(200))
        QTimer.singleShot(6000, lambda: self.heartbeat_animation.set_speed(700))
        QTimer.singleShot(9000, lambda: self.heartbeat_animation.set_speed(500))

    def apply_isoprenalina_effect(self):
        self.heart_rate_graph.apply_drug("Isoprenalina 20mcg")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Isoprenalina: </b>Estimulante beta, provoca acentuada taquicardia, vasodilatação e queda da PA. Rapidamente capturada pelos tecidos.")
        QTimer.singleShot(3000, lambda: self.heartbeat_animation.set_speed(100))
        QTimer.singleShot(4000, lambda: self.heartbeat_animation.set_speed(700))

    
    def apply_efedrina_effect(self):
        self.heart_rate_graph.apply_drug("Efedrina 5mg")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Efedrina:</b> Pouca atuação em receptores beta. Ligeira taquicardia e hipertensão um pouco acentuada. Absorção mais demorada.")
        QTimer.singleShot(5000, lambda: self.heartbeat_animation.set_speed(500))
        QTimer.singleShot(8000, lambda: self.heartbeat_animation.set_speed(700))
    
    def apply_acetilcolina_effect(self):
        self.heart_rate_graph.apply_drug("Acetilcolina 20mcg")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Acetilcolina: </b>Atuação nos receptores muscarínicos. Provoca bradicardia e vasodilatação, resultando em queda da PA.<br> Ação rápida pela degradação por acetilcolinesterase.")
        QTimer.singleShot(2000, lambda: self.heartbeat_animation.set_speed(900))
        QTimer.singleShot(4000, lambda: self.heartbeat_animation.set_speed(700))

    def apply_pilocarpina_effect(self):
        self.heart_rate_graph.apply_drug("Pilocarpina 1,5mg")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Pilocarpina: </b>Estimula receptores muscarínicos, provocando bradicardia e vasodilatação, levando a queda de PA. <br>Ação mais duradoura por não ser metabolizada por colinesterases.")
        QTimer.singleShot(3000, lambda: self.heartbeat_animation.set_speed(800))
        QTimer.singleShot(6000, lambda: self.heartbeat_animation.set_speed(700))
        

    def apply_alfabloqueador_effect(self):
        self.heart_rate_graph.apply_drug("Alfabloqueador")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Alfabloqueador: </b>Bloqueio dos receptores alfa, provocando vasodilatação e hipotensão.<br> Na presença de, primeiro, noradrenalina, há uma pequena taquicardia e elevação da PA. <br>Posteriormente, na presença de Adrenalina, há vasodilatação e provoca hipotensão.")  
        QTimer.singleShot(2000, lambda: self.heartbeat_animation.set_speed(700))  
        QTimer.singleShot(3000, lambda: self.heartbeat_animation.set_speed(400))  
        QTimer.singleShot(3500, lambda: self.heartbeat_animation.set_speed(600))  
        QTimer.singleShot(5000, lambda: self.heartbeat_animation.set_speed(500))  
        
    def apply_neostigmina_effect(self):
        self.heart_rate_graph.apply_drug("Neostigmina 0,5mg")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Nesotigmina: </b>Afeta as enzimas que degradam a acetilcolina, causando uma ação mais demorada dela.<br> Provoca uma ligeira queda de PA e, ao administrar 20mcg de Acetilcolina,<br> há uma bradicardia intensa, hipotensão acentuada e aumento da duração do efeito da acetilcolina")
        QTimer.singleShot(2000, lambda: self.heartbeat_animation.set_speed(800))  
        QTimer.singleShot(3000, lambda: self.heartbeat_animation.set_speed(1000))  
        QTimer.singleShot(4000, lambda: self.heartbeat_animation.set_speed(700))  
    
    def apply_nicotina_effect(self):
        self.heart_rate_graph.apply_drug("Nicotina 300mg")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Nicotina: </b>Atua como estimulante ganglionar, liberando Na nos neurônios pela atuação nos receptores de Ac. <br>Provoca bradicardia e queda da PA ao se ligar aos gânglios parassimpáticos. <br>Ao se ligar aos gânglios simpáticos, provoca taquicardia e hipertensão") 
        QTimer.singleShot(2000, lambda: self.heartbeat_animation.set_speed(800))  
        QTimer.singleShot(3000, lambda: self.heartbeat_animation.set_speed(400))  
        QTimer.singleShot(3500, lambda: self.heartbeat_animation.set_speed(500))  
        QTimer.singleShot(5000, lambda: self.heartbeat_animation.set_speed(700))
    
    def apply_propanolol_effect(self):
        self.heart_rate_graph.apply_drug("Propanolol 10mg")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Propanolol: </b>Bloqueia os receptores beta 1 e 2. Causa bradicardia e vasoconstrição na área dos músculos esqueléticos. <br>Na presença de Isoprenalina, não se altera a FC e a PA. <br> Na presença de NA e AD, há apenas o aumento da PA") 
        QTimer.singleShot(2000, lambda: self.heartbeat_animation.set_speed(800))  
   

    def apply_atropina_effect(self):
        self.heart_rate_graph.apply_drug("Atropina 10mg")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Atropina: </b>Bloqueia os receptores muscarínicos. Provoca taquicardia, pois a noradrenalina atua sem o bloqueio da acetilcolina.<br> Com o bloqueio, a administração de 20mcg de Acetilcolina é ineficaz. <br>A aplicação de 2mg de Acetilcolina provoca estímulo ganglionar, liberando noradrenalina nos tecidos, provocando taquicardia e hipertensão.") 
        QTimer.singleShot(2000, lambda: self.heartbeat_animation.set_speed(500))  
        QTimer.singleShot(3000, lambda: self.heartbeat_animation.set_speed(400))   
        QTimer.singleShot(5000, lambda: self.heartbeat_animation.set_speed(700))

    def apply_hexametonio_effect(self):
        self.heart_rate_graph.apply_drug("Hexametonio 20mg")
        self.heartbeat_animation.set_speed(700)
        self.legend_label.setText("<b>Hexametonio: </b>Bloqueador ganglionar, provoca taquicardia e hipotensão. Mesmo ao aplicar a Nicotina e 2mg de Acetilcolina, <br>pelo bloqueio ganglionar, não apresentam efeito.") 
        QTimer.singleShot(2000, lambda: self.heartbeat_animation.set_speed(500))  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    simulator = HeartSimulator()
    simulator.showFullScreen()  # Altera para modo tela cheia
    simulator.show()
    sys.exit(app.exec_())

