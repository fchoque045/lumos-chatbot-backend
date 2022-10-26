import {
  fetchSaludoBienvenida,
  fetchDespedida,
  fetchGenerico,
  fetchCategorias,
  fetchSubcategoriasByCategoria,
  fetchSubcategoriasByIdSubcategoria,
  fetchQuestionByIdSubcategoria,
  fetchQuestion,
  fetchQuestionByKeyword,
} from "./services.js";

class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };

    this.hello = true;
    this.state = false;
  }

  async setSaludoBienvenida() {
    try {
      const msj = await fetchSaludoBienvenida();
      const message_bot = { name: "bot", message: msj.mensaje };
      // await this.displayWait();
      this.updateChatText(this.args.chatBox, message_bot);
    } catch (error) {
      const message_bot = { name: "bot", message: "Error" };
      this.updateChatText(this.args.chatBox, message_bot);
    }
  }

  async setSaludoPresentacion(name) {
    try {
      const msj = await fetchGenerico("MPre");
      const data = await fetchCategorias();
      await this.displayWait();
      this.displayCategory(data, msj.texto.replace("{name}", name));
      this.hello = false;
    } catch (error) {
      const message_bot = { name: "bot", message: "Error" };
      this.updateChatText(this.args.chatBox, message_bot);
    }
  }

  initializationButtons() {
    const { openButton, chatBox, sendButton } = this.args;
    openButton.addEventListener("click", () => this.toggleState(chatBox));
    sendButton.addEventListener("click", () => this.sendMessage(chatBox));

    const node = chatBox.querySelector("input");

    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.sendMessage(chatBox);
      }
    });
  }

  sendMessage(chatbox) {
    let textField = chatbox.querySelector("input");
    let text1 = textField.value;
    this.onSendButton(text1);
    textField.value = "";
  }

  toggleState(chatbox) {
    this.state = !this.state;

    // show or hides the box
    if (this.state) {
      chatbox.classList.add("chatbox--active");
      chatbox.classList.remove("oculto");
    } else {
      chatbox.classList.remove("chatbox--active");
      chatbox.classList.add("oculto");
    }
  }

  displayCategory(data, message) {
    data.forEach((c) => (c.type = "category"));
    const message_bot = { name: "bot", choices: data, message };
    this.updateChatText(this.args.chatBox, message_bot);
  }

  displaySubcategory(data, message) {
    data.forEach((s) => (s.type = "subcategory"));
    const message_bot = {
      name: "bot",
      choices: data,
      message: `Dudas respecto a ${message}`,
    };
    console.log(message_bot);
    this.updateChatText(this.args.chatBox, message_bot);
  }

  displaySubcategoryQuestion(data1, data2) {
    data1.forEach((s) => (s.type = "subcategory"));
    data2.forEach((p) => (p.type = "question"));
    const data = data1.concat(data2);
    const message_bot = {
      name: "bot",
      choices: data,
      message: `Selecciona una de las opciones`,
    };
    this.updateChatText(this.args.chatBox, message_bot);
  }

  displayQuestion(data) {
    const message_bot = {
      name: "bot",
      message: data.respuesta,
      type: "question",
    };
    this.updateChatText(this.args.chatBox, message_bot);
  }

  displayQuestionKeyword(data) {
    data.forEach((p) => (p.type = "question"));
    const message_bot = this.getMessageUser({ choices: data });
    message_bot.message = `Preguntas referidas a la consulta`;
    this.updateChatText(this.args.chatBox, message_bot);
  }

  displayWait() {
    const chatmessage = this.args.chatBox.querySelector(".chatbox__messages");
    chatmessage.appendChild(this.createWaitItem());
    chatmessage.scrollTop = chatmessage.scrollHeight;
    return new Promise((resolve) => {
      setTimeout(() => {
        const node = document.getElementById("wait__element");
        chatmessage.removeChild(node);
        resolve("resolved");
      }, 2000);
    });
  }

  async onSendButton(message) {
    if (!message) {
      return;
    }

    let msg1 = { name: "user", message };
    this.updateChatText(this.args.chatBox, msg1);

    if (this.hello) {
      this.setSaludoPresentacion(message);
      return;
    }

    try {
      const data = await fetchQuestionByKeyword(message);
      if (data.length != 0) {
        await this.displayWait();
        this.displayQuestionKeyword(data);
      }
      if (data.length == 0) {
        const bye = await fetchDespedida(message);
        if (bye.length != 0) {
          const message_bot = { name: "bot", message: bye.mensaje };
          await this.displayWait();
          this.updateChatText(this.args.chatBox, message_bot);
        } else {
          const msj = await fetchGenerico("MDef");
          const categories = await fetchCategorias(msj.texto);
          await this.displayWait();
          this.displayCategory(categories, msj.texto);
        }
      }
    } catch (error) {
      return;
    }
  }

  async onClickChoice(message, type, id) {
    const { chatBox } = this.args;
    let msg1 = { name: "user", message };
    this.updateChatText(chatBox, msg1);
    if (type == "category") {
      try {
        const data = await fetchSubcategoriasByCategoria(id);
        await this.displayWait();
        this.displaySubcategory(data, message);
      } catch (error) {
        console.log(error);
        console.log("Algo paso, no se pudo resolver...");
      }
    }

    if (type == "subcategory") {
      try {
        const data1 = await fetchSubcategoriasByIdSubcategoria(id);
        const data2 = await fetchQuestionByIdSubcategoria(id);
        await this.displayWait();
        this.displaySubcategoryQuestion(data1, data2);
      } catch (error) {
        return;
      }
    }

    if (type == "question") {
      try {
        const data = await fetchQuestion(id);
        await this.displayWait();
        this.displayQuestion(data);
      } catch (error) {
        console.log(error);
        console.log("Algo paso, no se pudo resolver...");
      }
    }
  }

  createMessageContent(children, clazz) {
    const messageItem = document.createElement("div");
    messageItem.classList.add("messages__container");
    if (clazz === "operator") {
      messageItem.classList.add("message__contaner--operator");
    }
    children.forEach((c) => messageItem.appendChild(c));
    return messageItem;
  }

  createMessageItem(clazz, content) {
    const messageElement = document.createElement("div");
    messageElement.innerHTML = content;
    messageElement.classList.add("messages__item");
    messageElement.classList.add(`messages__item--${clazz}`);
    return messageElement;
  }

  updateChatText(chatbox, item) {
    let messageChildren;
    const messageClass = item.name === "bot" ? "visitor" : "operator";
    if (item.choices) {
      messageChildren = this.createMessageItem(messageClass, item.message);
      item.choices.map((c) => {
        const item_choice = document.createElement("div");
        item_choice.textContent = c.descripcion ? c.descripcion : c.pregunta;
        item_choice.classList.add("message__item--choice");
        item_choice.addEventListener("click", () => {
          this.onClickChoice(item_choice.textContent, c.type, c.id);
        });
        messageChildren.appendChild(item_choice);
      });

      messageChildren = [messageChildren];
    } else {
      messageChildren = [this.createMessageItem(messageClass, item.message)];
    }

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.appendChild(
      this.createMessageContent(messageChildren, messageClass)
    );
    chatmessage.scrollTop = chatmessage.scrollHeight;
  }

  createWaitItem() {
    const messageElement = document.createElement("div");
    messageElement.setAttribute("id", "wait__element");
    messageElement.classList.add("messages__item");
    messageElement.classList.add(`messages__item--visitor`);
    const waitElement = document.createElement("div");
    waitElement.classList.add("dot-pulse");
    waitElement.classList.add("messages__container");
    const waitChildElement = document.createElement("div");
    waitChildElement.classList.add("dot-pulse__dot");
    messageElement.appendChild(waitElement);
    waitElement.appendChild(waitChildElement);
    return messageElement;
  }
}

const chatbox = new Chatbox();
chatbox.setSaludoBienvenida();
chatbox.initializationButtons();
