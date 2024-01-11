document.addEventListener("DOMContentLoaded", function () {
    const calendarContainer = document.getElementById("calendar");
    const daysContainer = document.getElementById("daysContainer");
    const currentMonthYearElement = document.getElementById("currentMonthYear");
    const prevMonthButton = document.getElementById("prevMonth");
    const nextMonthButton = document.getElementById("nextMonth");

    let currentDate = new Date();

    // Mapeamento de membros aos dias fixos da semana
    const memberSchedule = [
        { member: "André", dayOfWeek: 0, weekOfMonth: 1 },   // Primeiro domingo
        { member: "P", dayOfWeek: 1, weekOfMonth: 1 },    // Primeira segunda-feira
        { member: "", dayOfWeek: 2, weekOfMonth: 1 },  // Última sexta-feira
        { member: "Tatiele", dayOfWeek: 3, weekOfMonth: 1 },  // Última sexta-feira
        { member: "Nádia", dayOfWeek: 4, weekOfMonth: 1 },  // Última sexta-feira
        { member: "", dayOfWeek: 5, weekOfMonth: 1 },  // Última sexta-feira
        { member: "", dayOfWeek: 6, weekOfMonth: 1 },
        { member: "Bispo", dayOfWeek: 0, weekOfMonth: 2 },   // Primeiro domingo
        { member: "Y", dayOfWeek: 1, weekOfMonth: 2 },    // Primeira segunda-feira
        { member: "Fc Rocha", dayOfWeek: 2, weekOfMonth: 2 },  // Última sexta-feira
        { member: "Marcos", dayOfWeek: 3, weekOfMonth: 2 },  // Última sexta-feira
        { member: "Vanda", dayOfWeek: 4, weekOfMonth: 2 },  // Última sexta-feira
        { member: "Antônia", dayOfWeek: 5, weekOfMonth: 2 },  // Última sexta-feira
        { member: "Fátima", dayOfWeek: 6, weekOfMonth: 2 },  // Última sexta-feira
        { member: "Moroni", dayOfWeek: 0, weekOfMonth: 3 },   // Primeiro domingo
        { member: "D", dayOfWeek: 1, weekOfMonth: 3 },    // Primeira segunda-feira
        { member: "Nayra", dayOfWeek: 2, weekOfMonth: 3 },  // Última sexta-feira
        { member: "Sônia", dayOfWeek: 3, weekOfMonth: 3 },  // Última sexta-feira
        { member: "Âmparo", dayOfWeek: 4, weekOfMonth: 3 },  // Última sexta-feira
        { member: "Eleneide", dayOfWeek: 5, weekOfMonth: 3 },  // Última sexta-feira
        { member: "Germane", dayOfWeek: 6, weekOfMonth: 3 },
        { member: "Ivonete", dayOfWeek: 0, weekOfMonth: 4 },   // Primeiro domingo
        { member: "A", dayOfWeek: 1, weekOfMonth: 4 },    // Primeira segunda-feira
        { member: "Benildes", dayOfWeek: 2, weekOfMonth: 4 },  // Última sexta-feira
        { member: "Welton", dayOfWeek: 3, weekOfMonth: 4 },  // Última sexta-feira
        { member: "Jucirene", dayOfWeek: 4, weekOfMonth: 4 },  // Última sexta-feira
        { member: "João pedro", dayOfWeek: 5, weekOfMonth: 4 },  // Última sexta-feira
        { member: "Ricardo", dayOfWeek: 6, weekOfMonth: 4 },
        { member: "Silvana", dayOfWeek: 0, weekOfMonth: 5 },   // Primeiro domingo
        { member: "Y", dayOfWeek: 1, weekOfMonth: 5 },    // Primeira segunda-feira
        { member: "", dayOfWeek: 2, weekOfMonth: 5 },  // Última sexta-feira
        { member: "", dayOfWeek: 3, weekOfMonth: 5 },  // Última sexta-feira
        { member: "", dayOfWeek: 4, weekOfMonth: 5 },  // Última sexta-feira
        { member: "", dayOfWeek: 5, weekOfMonth: 5 },  // Última sexta-feira
        { member: "", dayOfWeek: 6, weekOfMonth: 5 },
        // Adicione mais membros e regras conforme necessário
    ];

    // Função para preencher o calendário
    function renderCalendar() {
        const daysInMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
        const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();

        currentMonthYearElement.textContent = `${getMonthName(currentDate.getMonth())} ${currentDate.getFullYear()}`;

        daysContainer.innerHTML = "";

        // Adicione dias vazios até o primeiro dia do mês
        for (let i = 0; i < firstDayOfMonth; i++) {
            const emptyDay = document.createElement("div");
            emptyDay.classList.add("day", "empty");
            daysContainer.appendChild(emptyDay);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement("div");
            dayElement.classList.add("day");
            const numberElement = document.createElement("div");
            numberElement.classList.add("day-number");
            numberElement.textContent = day;
            dayElement.appendChild(numberElement);

            const scheduledMember = getMemberForDay(day);
            if (scheduledMember) {

                const nameElement = document.createElement("div");
                nameElement.classList.add("day-name");
                nameElement.textContent = scheduledMember.member;
                dayElement.appendChild(nameElement);
            }

            // Exemplo: Adiciona um evento de clique para simular interatividade
            dayElement.addEventListener("click", function () {
                alert(`Clique no dia ${day}. Membro agendado: ${scheduledMember ? scheduledMember.member : 'Nenhum membro agendado'}`);
            });

            daysContainer.appendChild(dayElement);
        }
    }

    // Função para obter o nome do mês
    function getMonthName(month) {
        const monthNames = [
            "Janeiro", "Fevereiro", "Março",
            "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro",
            "Outubro", "Novembro", "Dezembro"
        ];
        return monthNames[month];
    }

    // Função para obter o membro agendado para o dia específico
    function getMemberForDay(day) {
        const dayOfWeek = new Date(currentDate.getFullYear(), currentDate.getMonth(), day).getDay();
        
        for (const schedule of memberSchedule) {
            const targetDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
            targetDate.setDate(targetDate.getDate() + (schedule.dayOfWeek - targetDate.getDay() + 7) % 7 + (schedule.weekOfMonth - 1) * 7);

            if (targetDate.getDate() === day && targetDate.getMonth() === currentDate.getMonth()) {
                return { member: schedule.member, dayOfWeek: schedule.dayOfWeek, weekOfMonth: schedule.weekOfMonth };
            }
        }

        return null;
    }

    // Adicione eventos aos botões de navegação
    prevMonthButton.addEventListener("click", function () {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    nextMonthButton.addEventListener("click", function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    // Chame a função para preencher o calendário
    renderCalendar();
});
