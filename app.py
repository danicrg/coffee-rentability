import streamlit as st
import pandas as pd

st.image('https://thesourcebulkfoods.com.au/wp-content/uploads/2017/09/60101-Coffee-Beans.jpg', use_column_width=True)

st.title('Calculadora de inversión en una nueva cafetera de grano :coffee:')

st.subheader(':page_with_curl: Datos de la cafetera actual')

per_coffee_cost = st.number_input('Coste por café (€)', 0.0, 10.0, 0.40)
n_coffees_per_day = st.slider('Cafés diarios', 1, 20, 7)

st.subheader(':page_facing_up: Datos de la nueva cafetera')

machine_cost = st.number_input('Coste de la nueva cafetera (€)', 0.0, 2000.0, 200.0)
coffee_bag_cost = st.number_input('Coste de una bolsa de granos de café (€)', 0.0, 30.0, 5.0)
n_servins_per_bag = st.number_input('Número de tazas por bolsa', 0, 400, 100)
N_YEARS_FORWARD = int(st.slider('Vida útil de la cafetera (años)', 10, 40, 20))

new_per_coffee_cost = coffee_bag_cost / n_servins_per_bag

times_cheaper = int(-(-per_coffee_cost/new_per_coffee_cost))

st.markdown(f'Cada taza cuesta **{round(new_per_coffee_cost, 3)} €** en la nueva máquina, **{times_cheaper} veces más barato** que con tu máquina actual.')

st.subheader(':chocolate_bar: Amortización de la compra')

st.markdown('Cada día, el coste medio diario de haber comprado una nueva máquina se irá reduciendo, ya que el desembolso de la compra de la máquina es solo el primer día. En el momento en que coincide el coste medio diario con el de la antigua máquina estará amortizada la compra y comenzarás a ahorrar.')

amortization_time = int((machine_cost + -new_per_coffee_cost*n_coffees_per_day)//((per_coffee_cost-new_per_coffee_cost)*n_coffees_per_day))

N_POINTS = 365*N_YEARS_FORWARD

data = pd.DataFrame()
data['new_cost_per_day'] = [machine_cost] + [new_per_coffee_cost*n_coffees_per_day]*(N_POINTS-1)
data['actual_cost_per_day'] = [per_coffee_cost*n_coffees_per_day]*N_POINTS
data['new_cost'] = data['new_cost_per_day'].expanding().mean()
data['days'] = data.index
data['savings'] = (data['actual_cost_per_day'] - data['new_cost_per_day'])
data['savings'] = data['savings'].expanding().sum()

st.vega_lite_chart(data[:int(amortization_time*2)], {
	"width": "container",
  	"height": 400,
	"layer": [{
		"mark": {"type": "line", "color": "#85C5A6"},
		"encoding": {
			"x": {"field": "days", "type": "quantitative", "title": "Días"},
			"y": {"field": "new_cost", "type": "quantitative", "scale": {"type": "log"}, "title": "Nuevo coste medio"}
		}
	}, {
    	"mark": {"type": "line", "color": "#FF6961"},
		"encoding": {
			"x": {"field": "days", "type": "quantitative"},
			"y": {"field": "actual_cost_per_day", "type": "quantitative", "scale": {"type": "log"}, "title": "Coste actual medio"}
		}
	}]
}, use_container_width=True)


st.markdown(f'En **{round(amortization_time)} días** estará amortizada la máquina de café.')

st.subheader(':euro: Ahorro por la nueva cafetera')

st.vega_lite_chart(data[:int(amortization_time*2)], {
	"width": "container",
  	"height": 300,
	"mark": {"type": "line", "color": "#85C5A6"},
	"encoding": {
		"x": {"field": "days", "type": "quantitative", "title": "Días"},
		"y": {"field": "savings", "type": "quantitative", "title": "Dinero ahorrado (€)"}
	}
	
}, use_container_width=True)

total_savings = data['savings'].values[-1]
average_savings = total_savings/N_YEARS_FORWARD

st.markdown(f'Cada año ahorrarás de media **{round(average_savings, 2)} €**')

st.markdown(f'En la vida útil de la máquina ({N_YEARS_FORWARD} años) ahorrarás **{round(total_savings, 2)} €**')

st.markdown('------')
st.markdown(':computer: by [Daniel Carlander](https://github.com/danicrg/). Code available in [GitHub](https://github.com/danicrg/coffee-rentability)')