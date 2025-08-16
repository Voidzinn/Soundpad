remember_buttons();

const contextMenu = document.getElementById('contextMenu');
var buttons = document.querySelectorAll('.added-buttons');
const renameModal = document.getElementById("renameModal");
const newButtonModal = document.getElementById("newButtonModal");
const newSoundModal = document.getElementById("newSoundModal");
let clickedElement = null;

// _________________________________________ GENERAL PURPOSE FUNCTIONS _________________________________________ \\

// Show context menu
buttons.forEach(button => {
    button.addEventListener("contextmenu", function(event) 
    {
        event.preventDefault();
        clickedElement = event.currentTarget;
        showContextMenu(event.pageX, event.pageY);
    });
});

function showContextMenu(x, y)
{
  contextMenu.style.top = `${y}px`;
  contextMenu.style.left = `${x}px`;
  contextMenu.style.display = "block";
};

// Hide context menu
document.addEventListener("click", function()
{
    if(contextMenu.style.display === "block")
    {
        contextMenu.style.display = "none";
    }
});

// ______________________________________________ RENAME MODAL ______________________________________________ \\

// Change button's text
function rename_button()
{
    let original_text = clickedElement.textContent;
    let new_name = document.getElementById("newNameInput").value.trim();
    if(new_name === original_text)
    {
        send_error('O nome inserido é igual o nome original.');
    }
    else if(!new_name)
    {
        send_error('Ocorreu um erro. Certifique-se que o nome inserido não está vazio.');
    }
    else
    {
        if(clickedElement.classList.value.includes('created-buttons'))
        {
            eel.update_button_name(clickedElement.dataset.file, new_name);
        }
        clickedElement.textContent = new_name;
        send_notification(`Nome do botão alterado com sucesso.`);
    }
    close_rename_modal();
};

// Open the rename modal
function open_rename_modal()
{
    let input = document.getElementById("newNameInput");

    renameModal.style.display = "block";
    input.value = clickedElement.textContent;
    input.focus();
}

// Close the rename modal (general)
function close_rename_modal()
{
    if(renameModal.style.display === "block")
    {
        renameModal.style.display = "none";
    }
}

// Close the rename modal (screen click)
document.addEventListener("click", (event) =>{
    if(event.target === renameModal)
    {
        close_rename_modal();
    }
});

// ______________________________________________ NEW BUTTON MODAL ______________________________________________ \\

// Open the new button modal
function open_new_button_modal()
{
    newButtonModal.style.display = "block";
    document.getElementById("newButtonNameInput").focus();
}

// Close the new button modal (general)
function close_new_button_modal()
{
    if(newButtonModal.style.display === "block")
    {
        newButtonModal.style.display = "none";
    }
}

// Close the rename modal (screen click)
document.addEventListener("click", (event) =>{
    if(event.target === newButtonModal)
    {
        close_new_button_modal();
    }
});

// ______________________________________________ NEW SOUND MODAL ______________________________________________ \\

// Open the new sound modal
function open_new_sound_modal()
{
    newSoundModal.style.display = "block";
    document.getElementById("oldSoundFileShow").value = `Som atual: ${clickedElement.dataset.file}`;
}

// Close the new sound modal (general)
function close_new_sound_modal()
{
    if(newSoundModal.style.display === "block")
    {
        newSoundModal.style.display = "none";
    }
}

// Close the sound modal (screen click)
document.addEventListener("click", (event) =>{
    if(event.target === newSoundModal)
    {
        close_new_sound_modal();
    }
});

async function change_sound() {
    let new_sound_file = document.getElementById("newSoundFileInput").files[0]

    if(!new_sound_file)
    {
        send_error("O arquivo não foi selecionado")
    }

    let new_sound_name = new_sound_file.name

    let buffer = await new_sound_file.arrayBuffer();
    let bytes = Array.from(new Uint8Array(buffer));
    
    let response = await eel.change_button_sound(clickedElement.dataset.file, new_sound_name, bytes)();

    if(response.success)
    {
        clickedElement.dataset.file = new_sound_name;
        send_notification(response.message);
    }
    else
    {
        send_error(response.message);
    }
    close_new_sound_modal();
}

// ______________________________________________ BUTTON FUNCTION ______________________________________________ \\

// Create new button
async function create_new_button()
{
    let new_button_name = document.getElementById("newButtonNameInput").value.trim();
    let new_button_file = document.getElementById("newButtonFileInput").files[0];
    let file_name = new_button_file.name

    if(!new_button_file || !new_button_name)
    {
        send_error("Ambos os campos devem estar preenchidos.");
        return;
    }

    let buffer = await new_button_file.arrayBuffer();
    let bytes = Array.from(new Uint8Array(buffer));

    let response = await eel.create_new_button(new_button_name, file_name, bytes)();

    if(response.success)
    {
        close_new_button_modal();
        create_button(new_button_name, file_name);
        send_notification(response.message);
    }
    else
    {
        send_error(response.message);
    }
}

// Create button (general)
function create_button(button_name, button_file)
{
    let newbtn = document.createElement("button");
    newbtn.textContent = button_name;
    newbtn.dataset.file = button_file;
    newbtn.classList = "added-buttons created-buttons";
    newbtn.onclick = function() { play_sound(this) };
    
    document.getElementById("buttons").insertBefore(newbtn, document.getElementById("new-button"));
    
    newbtn.addEventListener("contextmenu", function(event) {
        event.preventDefault();
        clickedElement = event.currentTarget;
        showContextMenu(event.pageX, event.pageY);
    });
    
    buttons = document.querySelectorAll('.added-buttons');
}

async function delete_button()
{
    let button_file = clickedElement.dataset.file;
    result = await eel.delete_button(button_file)();

    if(result.success)
    {
        clickedElement.remove();
    }
    else
    {
        send_error(result.message);
    }
}

// Play sound (in design)
async function play_sound(btn)
{
    buttons.forEach(button => button.disabled = true);
    document.getElementById('stopButton').classList.replace('hidden', 'active')

    sound_name = btn.dataset.file

    const original_text = btn.textContent;
    btn.textContent = 'Tocando...';

    try 
    {
        send_notification(`Tocando o som: ${sound_name}`)
        await eel.play_sound(sound_name)();
    }
    catch (error)
    {
        send_error('Ocorreu um erro');
        console.error('Ocorreu um erro: ', error);
    }

    let check = setInterval(async () => 
        {
            let playing = await eel.is_playing()();

            if(!playing)
            {
                clearInterval(check);
                btn.textContent = original_text;
                buttons.forEach(button => button.disabled = false);
                document.getElementById('stopButton').classList.replace('active', 'hidden')
            }
        }, 200);
};


// DOCUMENT LOAD
window.addEventListener('DOMContentLoaded', () => {
    window.onresize = function() {
        window.resizeTo(1920, 1080);
    };
});

// _______________________________________________ EEL FUNCTIONS _______________________________________________ \\ 

const notificationContainer = document.getElementById("notificationContainer");

function showScreen(screenId)
{
    document.querySelectorAll(".screen").forEach(screen => screen.classList.remove("active"));
    document.getElementById(screenId).classList.add("active");
};

eel.expose(showScreen);

// ________________________________________________ NOTIFICATIONS ________________________________________________ \\

function send_notification(message)
{
    let notification = document.createElement("div");

    notification.className = "notification";
    notification.textContent = message;

    notificationContainer.appendChild(notification);

    setTimeout(() => {notification.remove()}, 4000);
};

function send_error(message)
{
    let error = document.createElement("div");

    error.className = "error";
    error.textContent = message;

    notificationContainer.appendChild(error);

    setTimeout(() => {error.remove()}, 4000);
};

eel.expose(send_notification);
eel.expose(send_error);

// "REMEMBER" buttons
async function remember_buttons()
{
    for(const {file, name} of Object.values(JSON.parse(await eel.get_config_data()()).created_buttons))
    {
        create_button(name, file);
    }
}
