from django import forms
from crispy_forms.helper import FormHelper,Layout
from crispy_forms.layout import Submit,Field
from crispy_forms.bootstrap import  FormActions

class ControlPanel(forms.Form):
	ticker = forms.CharField(label="Ticker",required=True)
	start_date = forms.CharField(label="Start Date",required=True)
	end_date = forms.CharField(label="End Date",required=True)
	#create form helper
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_id = 'GenImgForm'
	helper.form_action = "/generate-image/"
    #helper.form_class = 'well'
	#helper.add_input(Submit('build_graph','Build Graph',css_class='btn-primary'))
	component0=Field('ticker',css_class='input-xlarge',id='tickerIn')
	component1=Field('start_date',css_class='input-xlarge',id='start_date')
	component2=Field('end_date',css_class='input-xlarge',id='end_date')

	component3=Submit('build_graph','Build Graph',css_class='btn-primary')

	helper.layout = Layout(component0,component1,component2,FormActions(component3))