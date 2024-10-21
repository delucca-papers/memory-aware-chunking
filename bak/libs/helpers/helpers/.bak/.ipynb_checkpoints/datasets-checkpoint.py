def __ricker_wavelet(frequency: int, length: int, dt: float) -> np.ndarray:
    t = np.linspace(-length / 2, (length / 2) - dt, length) * dt
    y = (1 - 2 * (np.pi**2) * (frequency**2) * (t**2)) * np.exp(
        -(np.pi**2) * (frequency**2) * (t**2)
    )

    return y