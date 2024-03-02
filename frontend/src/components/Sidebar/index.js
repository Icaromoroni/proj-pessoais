import '../../index.css';
import { useState } from 'react';

function SideBar() {

  const[open, setOpen] = useState(true)
  const [active, setActive] = useState(0)
  const Menus = [
    { title : "Início", name:"home", gap: true},
    { title : "Painel", name:"space_dashboard", gap: true},
    { title : "Mensagens", name:"message"},
    { title : "Contas", name:"person_book", gap: true},
    { title : "Agendar", name:"calendar_clock"},
    { title : "Pesquisar", name:"search"},
    { title : "Análise", name:"chart_data"},
    { title : "Arquivos", name:"file_open", gap: true},
    { title : "Configurações", name:"settings"},
  ]

  console.log(active)

  return (
    <div className='flex'>
      <div className={`${
        open ? "w-72" : "w-20"
        } duration-300 p-5 pt-2 h-screen bg-dark-purple relative`}>
        <span className={`material-symbols-outlined absolute cursor-pointer rounded-full bg-white 
        -right-3 top-9 w-7 border-2 border-dark-purple ${!open && "rotate-180"}`}
        onClick={() => setOpen(!open)}>
        chevron_left
        </span>
        <div className='flex gap-x-4 items-center'>
          <img src='./logo192.png' className={`cursor-pointer duration-500 w-10 ${ open && "rotate-[360deg]"}`} alt=''/>
          <h1 className={`text-white font-medium text-xl 
          duration-300 ${!open && "scale-0"}`}>SPmotos</h1>
        </div>
          <ul>
            {Menus.map((menu, index) => (
              <li key={index} onClick={() => setActive(index)} className={`text-gray-300 text-sm cursor-pointer p-1 hover:bg-sky-700 rounded-md ${menu.gap ? "mt-9" : "mt-2"} ${index === active && "bg-sky-700"}`}>
                <a href='#' className={`flex items-center gap-x-4`}>
                <span className={`material-symbols-outlined text-green-500`}>{menu.name}</span>
                <span className={`${!open && 'hidden'} origin-left duration-200`}>{menu.title}</span>
                </a>
              </li>
            ))
            }
          </ul>
      </div>
      <div className='p-7 text-2x1 font-semibold flex-1 h-screen'>
        <h1>Home page</h1>
      </div>
    </div>
  );
}

export default SideBar;