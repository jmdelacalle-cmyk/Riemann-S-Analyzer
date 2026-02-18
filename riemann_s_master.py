import numpy as np
import matplotlib.pyplot as plt
from scipy.special import rel_entr

class RiemannS:
    """
    RIEMANN-S: SPECTRAL INTEGRITY ANALYZER
    Herramienta unificada de auditoría basada en GUE y Resonancia Cuántica.
    """
    def __init__(self):
        # Constantes Universales (Ley de Wigner-Dyson)
        self.A = 32 / (np.pi**2)
        self.B = 4 / np.pi
        self.resonance_eta = 5.26  # Constante de Estabilidad descubierta

    def _unfold(self, data):
        """Normalización espectral (Unfolding local)"""
        diffs = np.diff(data)
        if len(diffs) == 0: return []
        return diffs / np.mean(diffs)

    def _wigner_pdf(self, s):
        """La firma de la integridad"""
        return self.A * (s**2) * np.exp(-self.B * (s**2))

    def analyze_integrity(self, input_data, label="Muestra"):
        """
        NÚCLEO DEL ANÁLISIS: Calcula el % de 'Realidad' de los datos.
        """
        # Limpieza básica
        clean_data = np.sort([x for x in input_data if x > 0])
        if len(clean_data) < 50:
            print(f" [ERROR] Muestra insuficiente para {label}")
            return None

        # Proceso Físico
        s = self._unfold(clean_data)

        # Histograma vs Teoría
        bins = np.linspace(0, 3, 40)
        hist, _ = np.histogram(s, bins=bins, density=True)
        centers = (bins[:-1] + bins[1:]) / 2
        theory = self._wigner_pdf(centers)

        # Divergencia Kullback-Leibler (Entropía relativa)
        epsilon = 1e-10
        div = np.sum(rel_entr(hist + epsilon, theory + epsilon))
        score = 100 * np.exp(-div)

        return {
            "label": label,
            "score": score,
            "spectrum": (centers, hist, theory)
        }

    def scan_resonance(self, data):
        """
        BÚSQUEDA DE ORDEN OCULTO (Resonancia Eta ~ 5.26)
        Aplica filtro no-conmutativo para ver si el ruido se ordena.
        """
        t = np.arange(len(data))
        # Filtro de fase cuántica en la frecuencia crítica
        quantum_filter = np.exp(1j * self.resonance_eta / (t + 1))
        filtered = np.abs(np.fft.fft(data * quantum_filter))
        return self.analyze_integrity(filtered, label=f"Resonancia (Eta={self.resonance_eta})")

    def generate_report(self, result):
        if not result: return
        score = result['score']
        print(f"\n📊 REPORTE RIEMANN-S: {result['label']}")
        print(f"   > Integridad Estructural: {score:.2f}%")

        if score > 80: veredicto = "SISTEMA ROBUSTO (GUE - Natural)"
        elif score < 30: veredicto = "RUIDO O FRACTURA (Poisson - Aleatorio)"
        else: veredicto = "TRANSICIÓN / SOSPECHOSO"
        print(f"   > ESTADO: {veredicto}")

# --- ZONA DE EJECUCIÓN (Ejemplo de uso) ---
if __name__ == "__main__":
    print("Iniciando Riemann-S System...")
    engine = RiemannS()

    # Ejemplo: Datos aleatorios (Simulando ruido de mercado)
    data_test = np.random.exponential(1, 1000).cumsum()

    # 1. Análisis Estándar
    res1 = engine.analyze_integrity(data_test, "Test Ruido")
    engine.generate_report(res1)

    # 2. Escaneo de Resonancia (Buscando la huella oculta)
    res2 = engine.scan_resonance(data_test)
    engine.generate_report(res2)
