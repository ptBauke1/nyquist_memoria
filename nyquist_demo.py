import numpy as np
import matplotlib.pyplot as plt

# Função de reconstrução pelo método sinc
def sinc_reconstruction(t, t_samples, x_samples, fs):
    """
    Reconstrução de um sinal usando interpolação sinc.
    t          -> vetor de tempo onde será reconstruído
    t_samples  -> tempos das amostras
    x_samples  -> valores das amostras
    fs         -> taxa de amostragem
    """
    T = 1 / fs
    y = np.zeros_like(t)
    for n, tn in enumerate(t_samples):
        y += x_samples[n] * np.sinc((t - tn) / T)
    return y

# Parâmetros do sinal
f_sinal = 80          # Hz
fs_original = 10000    # "contínuo"
fs_nyquist = 450      # taxa de Nyquist (> 2*f_sinal)
duracao = 0.01         # segundos

# Tempo do sinal original
t_original = np.arange(0, duracao, 1/fs_original)
sinal_original = np.sin(2 * np.pi * f_sinal * t_original)

# Amostras
t_amostrado = np.arange(0, duracao, 1/fs_nyquist)
sinal_amostrado = np.sin(2 * np.pi * f_sinal * t_amostrado)

# Reconstrução usando sinc
sinal_reconstruido = sinc_reconstruction(t_original, t_amostrado, sinal_amostrado, fs_nyquist)

# ===== PLOTS =====
plt.figure(figsize=(6, 5))

# 1 - Sinal original
plt.subplot(3, 1, 1)
plt.plot(t_original, sinal_original, 'b')
plt.title(f'Sinal Original de {f_sinal} Hz (Alta resolução)', fontsize = 20)
plt.ylabel('Amplitude')
plt.grid(True)

# 2 - Amostras
plt.subplot(3, 1, 2)
plt.stem(t_amostrado, sinal_amostrado, linefmt='r-', markerfmt='ro', basefmt=' ')
plt.title(f'Amostras na taxa de Nyquist ({fs_nyquist} Hz)', fontsize = 20)
plt.ylabel('Amplitude')
plt.grid(True)

# 3 - Reconstrução
plt.subplot(3, 1, 3)
plt.plot(t_original, sinal_reconstruido, 'g')
plt.title('Sinal Reconstruído (Interpolação Sinc)', fontsize = 20)
plt.ylabel('Amplitude')
plt.grid(True)

plt.tight_layout()
plt.show()
