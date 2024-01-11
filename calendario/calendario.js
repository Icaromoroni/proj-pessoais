const isLeapYear = (year) => {
    return(
        (year % 4 ===0 && year % 100 !== 0 && 400 !== 0) ||
        (year % 100 === 0 && year % 400 ===0)
    );
};

const getFebDays = (year) => {
    return isLeapYear(year) ? 29 : 28;
};

const month_names = [
    'Janeiro',
    'Fevereiro',
    'Março',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro'
];

const nomes_ = [
    'João',
    'Maria',
    'José',
    'André',
    'Antonia',
]
let month_picker = document.querySelector('#month');

const generateCalendar = (month, year) => {
    let calendar_days = document.querySelector('.calendar-days');
    calendar_days.innerHTML = '';
    let calendar_header_year = document.querySelector('#year');
    let days_of_month = [
        31,
        getFebDays(year),
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31
    ];
    let currentDate = new Date();
    month_picker.innerHTML = month_names[month];
    calendar_header_year.innerHTML = year;
    let first_day = new Date(year, month);
    let semana = new Date()

    for(let i=0; i<=days_of_month[month] + first_day.getDay() - 1; i++){
        let day = document.createElement('div');
        let nomes= document.createElement('p');
        let numDay = document.createElement('span');
        if(i>=first_day.getDay()){
            numDay.innerHTML = i - first_day.getDay() + 1;
            // nomes.innerHTML = nomes_[(i - first_day.getDay() + 1)-first_day.getDay() + 1]
            if(i - first_day.getDay() + 1 === currentDate.getDate() && year === 
            currentDate.getFullYear() && month === currentDate.getMonth()){
                numDay.classList.add('current-date');

                
            }
        }
        day.appendChild(numDay)
        day.appendChild(nomes)
        calendar_days.appendChild(day);
    }
};

document.querySelector('#pre-month').onclick = () => {
    --currentMonth.value;
    if (currentMonth.value < 0){
        currentMonth.value = 11
        --currentYear.value
    }
    generateCalendar(currentMonth.value, currentYear.value);
};
document.querySelector('#next-month').onclick = () => {
    ++currentMonth.value;

    if (currentMonth.value > 11){
        currentMonth.value = 0
        ++currentYear.value
    }
    generateCalendar(currentMonth.value, currentYear.value)
};

let currentDate = new Date();
let currentMonth = {value: currentDate.getMonth()};
let currentYear = {value: currentDate.getFullYear()};
generateCalendar(currentMonth.value, currentYear.value);


const todayShowDate = document.querySelector('.date-formate');
const todayShowTime = document.querySelector('.time-formate');

const currshowDate = new Date();
const showCurrentDateOption = {
    year : 'numeric',
    month :'long',
    day : 'numeric',
    weekday : 'long'
};

const currentDateFormate = new Intl.DateTimeFormat(
    'pt-br',
    showCurrentDateOption
).format(currshowDate);

todayShowDate.textContent = currentDateFormate;
setInterval(()=>{
    const timer = new Date();
    const option = {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
    }
    const formateTime = new Intl.DateTimeFormat('pt-br', option).format(timer);
    let time = `${`${timer.getHours()}`.padStart(2, 0)}:
    ${`${timer.getMinutes()}`.padStart(2, 0)}:
    ${`${timer.getSeconds()}`.padStart(2, 0)}`;
    todayShowTime.textContent = formateTime;
}, 1000);