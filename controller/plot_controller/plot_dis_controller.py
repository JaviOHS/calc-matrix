import numpy as np

class PlotDistributionController:
    def __init__(self, manager, figure_manager, style_helper):
        self.manager = manager
        self.figure_manager = figure_manager
        self.style_helper = style_helper

    def create_epidemic_plot(self, times, susceptible, infected, recovered, params):
        """Crea un gráfico personalizado para la simulación de epidemias."""
        try:
            # Crear un nuevo canvas
            canvas = self.figure_manager.create_canvas(figsize=(10, 6))
            ax = canvas.ax
            
            # Aplicar estilo oscuro
            self.style_helper.apply_dark_style(canvas, ax)
            
            # Graficar las tres curvas
            ax.plot(times, susceptible, 
                   color=self.style_helper.get_plot_color(0),
                   label='Susceptibles', linewidth=2)
            ax.plot(times, infected, 
                   color=self.style_helper.get_plot_color(1),
                   label='Infectados', linewidth=2)
            ax.plot(times, recovered, 
                   color='#1E90FF',
                   label='Recuperados', linewidth=2)

            # Encontrar y marcar el pico de infectados
            max_infected_idx = np.argmax(infected)
            max_infected_time = times[max_infected_idx]
            max_infected_value = infected[max_infected_idx]
            
            # Añadir línea vertical en el pico
            ax.axvline(x=max_infected_time, color='gray', linestyle='--', alpha=0.5)
            ax.text(max_infected_time + 0.5, max_infected_value,
                   f'Pico: {int(max_infected_value)}',
                   color=self.style_helper.TEXT_COLOR)

            # Configurar etiquetas y título
            ax.set_xlabel('Tiempo (días)', color=self.style_helper.TEXT_COLOR)
            ax.set_ylabel('Población', color=self.style_helper.TEXT_COLOR)
            ax.set_title('Simulación de Epidemia (Modelo SIR)',
                        color=self.style_helper.TEXT_COLOR)

            # Análisis de R₀
            r0 = params.get('beta', 0) / params.get('gamma', 1)
            r0_text = f'R₀ = {r0:.2f}'
            r0_text += ' > 1 (Epidemia en crecimiento)' if r0 > 1 else ' < 1 (Epidemia en retroceso)'
            ax.set_xlabel(f'Tiempo (días) | {r0_text}', color=self.style_helper.TEXT_COLOR)

            # Configurar leyenda
            self.style_helper.configure_legend(ax)

            # Ajustar márgenes
            canvas.figure.subplots_adjust(bottom=0.2)

            return canvas

        except Exception as e:
            raise ValueError(f"Error al crear el gráfico de la epidemia: {str(e)}")