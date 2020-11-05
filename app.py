import streamlit as st
import pandas as pd

st.title('Should I buy a new coffee machine? :coffee:')
st.image('./coffee.jpg', use_column_width=True)

st.subheader(':page_with_curl: My current Coffee Machine')

per_coffee_cost = st.number_input('Cost per coffee (€)', 0.0, 10.0, 0.40)
n_coffees_per_day = st.slider('Coffees per day', 1, 20, 7)

st.subheader(':page_facing_up: [New Coffee Machine](https://amzn.to/2HbXDtn)')

machine_cost = st.number_input('New coffee machine cost (€)', 0.0, 2000.0, 200.0)
coffee_bag_cost = st.number_input('Cost of a bag of coffee grain (€)', 0.0, 30.0, 5.0)
n_servins_per_bag = st.number_input('Number of coffees per bag', 0, 400, 100)
N_YEARS_FORWARD = int(st.slider('Lifespan of coffee machine (years)', 10, 40, 20))

new_per_coffee_cost = coffee_bag_cost / n_servins_per_bag
times_cheaper = -(-per_coffee_cost/new_per_coffee_cost)


amortization_time = int((machine_cost + -new_per_coffee_cost*n_coffees_per_day)//((per_coffee_cost-new_per_coffee_cost)*n_coffees_per_day))

if amortization_time <= 0:
	st.markdown('The buy of a new machine would mean higher costs.')
else:

	st.markdown(f'Each coffee costs **{round(new_per_coffee_cost, 3)} €** with the new machine, **{round(times_cheaper, 1)} times cheaper** than with your current machine.')

	st.subheader(':chocolate_bar: Repayment of the purchase')
	st.markdown('- **Green Line:** Cummulative cost of new machine. It starts with the machine cost.\n' + 
		'- **Red Line:** Cummulative cost of the current machine.')
	st.markdown('When the lines cross you start saving.')


	N_POINTS = 365*N_YEARS_FORWARD

	data = pd.DataFrame()
	data['new_cost_per_day'] = [machine_cost] + [new_per_coffee_cost*n_coffees_per_day]*(N_POINTS-1)
	data['actual_cost_per_day'] = [per_coffee_cost*n_coffees_per_day]*N_POINTS
	data['new_cost'] = data['new_cost_per_day'].expanding().sum()
	data['actual_cost'] = data['actual_cost_per_day'].expanding().sum()
	data['days'] = data.index
	data['savings'] = (data['actual_cost_per_day'] - data['new_cost_per_day'])
	data['savings'] = data['savings'].expanding().sum()

	st.vega_lite_chart(data[:int(amortization_time*2)], {
		"width": "container",
	  	"height": 400,
		"layer": [{
			"mark": {"type": "line", "color": "#85C5A6"},
			"encoding": {
				"x": {"field": "days", "type": "quantitative", "title": "Days"},
				"y": {"field": "new_cost", "type": "quantitative", "title": ""}
			}
		}, {
	    	"mark": {"type": "line", "color": "#FF6961"},
			"encoding": {
				"x": {"field": "days", "type": "quantitative"},
				"y": {"field": "actual_cost", "type": "quantitative", "title": ""}
			}
		}]
	}, use_container_width=True)


	st.markdown(f'In **{round(amortization_time)} days** you will have repayed the new machine.')

	st.subheader(':euro: Savings calculations')

	st.vega_lite_chart(data[:int(amortization_time*2)], {
		"width": "container",
	  	"height": 300,
		"mark": "line",
		"encoding": {
			"x": {"field": "days", "type": "quantitative", "title": "Days"},
			"y": {"field": "savings", "type": "quantitative", "title": "Money saved (€)"}
		}
		
	}, use_container_width=True)

	total_savings = data['savings'].values[-1]
	average_savings = total_savings/N_YEARS_FORWARD

	st.markdown(f'Each year you will save in average **{round(average_savings, 2)} €**')

	st.markdown(f'In the lifespan of the machine ({N_YEARS_FORWARD} years) you will save **{round(total_savings, 2)} €**')

	st.markdown('------')
	st.markdown(':computer: by [Daniel Carlander](https://danielcarlander.com/?utm_source=coffee-rentability-dashboard&utm_medium=referral). Code available in [GitHub](https://github.com/danicrg/coffee-rentability)')
	st.markdown(':page_with_curl: Article [here](https://danielcarlander.com/coffee-rentability?utm_source=coffee-rentability-dashboard).')
