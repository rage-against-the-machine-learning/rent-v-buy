var down_payment_data = [0.0, 25000.0, 50000.0, 75000.0, 100000.0];
var downPaymentSlider = d3
    .sliderBottom()
    .min(d3.min(down_payment_data))
    .max(d3.max(down_payment_data))
    .width(300)
    .tickFormat(d3.format('($d'))
    .ticks(5)
    .default(40000.0)
    .on('onchange', val => {
        d3.select('p#value-down-payment').text(d3.format('($d')(val));
    });

var gSimple = d3
    .select('div#slider-down-payment')
    .append('svg')
    .attr('width', 500)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

gSimple.call(downPaymentSlider);
d3.select('p#value-down-payment').text(d3.format('($d')(downPaymentSlider.value()));

var mortgage_interest_data = [0.01, 0.03, 0.05, 0.07, 0.09];
var mortgageRateSlider = d3
    .sliderBottom()
    .min(d3.min(mortgage_interest_data))
    .max(d3.max(mortgage_interest_data))
    .width(300)
    .tickFormat(d3.format('.2%'))
    .ticks(5)
    .default(0.037)
    .on('onchange', val => {
        d3.select('p#value-mortgage-interest').text(d3.format('.2%')(val));
    });

var gSimple = d3
    .select('div#slider-mortgage-interest')
    .append('svg')
    .attr('width', 500)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

gSimple.call(mortgageRateSlider);
d3.select('p#value-mortgage-interest').text(d3.format('.2%')(mortgageRateSlider.value()));

var annual_maintenance_data = [0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0];
var maintenanceSlider = d3
    .sliderBottom()
    .min(d3.min(annual_maintenance_data))
    .max(d3.max(annual_maintenance_data))
    .width(300)
    .tickFormat(d3.format('($d'))
    .ticks(5)
    .default(1000.0)
    .on('onchange', val => {
        d3.select('p#value-annual-maintenance').text(d3.format('($d')(val));
    });

var gSimple = d3
    .select('div#slider-annual-maintenance')
    .append('svg')
    .attr('width', 500)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

gSimple.call(maintenanceSlider);
d3.select('p#value-annual-maintenance').text(d3.format('($d')(maintenanceSlider.value()));

var annual_home_insurance_data = [0.0, 500.0, 1000.0, 1500.0, 2000.0];
var homeInsuranceSlider = d3
    .sliderBottom()
    .min(d3.min(annual_home_insurance_data))
    .max(d3.max(annual_home_insurance_data))
    .width(300)
    .tickFormat(d3.format('($d'))
    .ticks(5)
    .default(1000.0)
    .on('onchange', val => {
        d3.select('p#value-annual-home-insurance').text(d3.format('($d')(val));
    });

var gSimple = d3
    .select('div#slider-annual-home-insurance')
    .append('svg')
    .attr('width', 500)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

gSimple.call(homeInsuranceSlider);
d3.select('p#value-annual-home-insurance').text(d3.format('($d')(homeInsuranceSlider.value()));