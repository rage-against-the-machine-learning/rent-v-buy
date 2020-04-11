/*
Inputs for financial calculations
Show only if a zip code has already been selected
*/
function showSliders(){
    // Down payment slider
    var down_payment_data = [0.0, 50000.0, 100000.0, 150000.0, 200000.0];
    var downPaymentSlider = d3
        .sliderBottom()
        .min(d3.min(down_payment_data)).max(d3.max(down_payment_data))
        .width(300)
        .tickFormat(d3.format('($,d'))
        .ticks(5)
        .default(40000.0)
        .on('onchange', val => { d3.select('p#value-down-payment').text(d3.format('($d')(val)); });
    var gSimple = d3
        .select('div#slider-down-payment')
        .append('svg')
        .attr('width', 500).attr('height', 75)
        .append('g')
        .attr('transform', 'translate(30,30)');
    gSimple.call(downPaymentSlider);
    d3.select('p#value-down-payment').text(d3.format('($d')(downPaymentSlider.value()));
    // Maintenance and HOA fees slider
    var annual_maintenance_data = [0.0, 5000.0, 10000.0, 15000.0, 20000.0];
    var maintenanceSlider = d3
        .sliderBottom()
        .min(d3.min(annual_maintenance_data)).max(d3.max(annual_maintenance_data))
        .width(300)
        .tickFormat(d3.format('($,d'))
        .ticks(5)
        .default(10000.0)
        .on('onchange', val => { d3.select('p#value-annual-maintenance').text(d3.format('($d')(val)); });
    var gSimple = d3
        .select('div#slider-annual-maintenance')
        .append('svg')
        .attr('width', 500).attr('height', 75)
        .append('g')
        .attr('transform', 'translate(30,30)');
    gSimple.call(maintenanceSlider);
    d3.select('p#value-annual-maintenance').text(d3.format('($d')(maintenanceSlider.value()));
    // Home insurance fees slider
    var annual_home_insurance_data = [0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0];
    var homeInsuranceSlider = d3
        .sliderBottom()
        .min(d3.min(annual_home_insurance_data)).max(d3.max(annual_home_insurance_data))
        .width(300)
        .tickFormat(d3.format('($,d'))
        .ticks(5)
        .default(3000.0)
        .on('onchange', val => { d3.select('p#value-annual-home-insurance').text(d3.format('($d')(val)); });
    var gSimple = d3
        .select('div#slider-annual-home-insurance')
        .append('svg')
        .attr('width', 500).attr('height', 75)
        .append('g')
        .attr('transform', 'translate(30,30)');
    gSimple.call(homeInsuranceSlider);
    d3.select('p#value-annual-home-insurance').text(d3.format('($d')(homeInsuranceSlider.value()));
}