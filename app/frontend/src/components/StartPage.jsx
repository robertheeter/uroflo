import App from "../App";
import { useState } from "react";
// import InputMask from "react-input-mask";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "react-dropdown/style.css";
import Keyboard from "react-simple-keyboard";
import "react-simple-keyboard/build/css/index.css";

const StartPage = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [sex, setSex] = useState("");
  const [date, setDate] = useState(null);
  const [MRN, setMRN] = useState("");
  const [contactA, setContactA] = useState("");
  const [contactB, setContactB] = useState("");

  const handleKeyPress = (button) => {
    if (button === "{shift}") handleClearClick();
    else if (button === "{bksp}") handleBackspaceClick();
    else if (button === "{space}") handleSpaceClick();
    else if (button === "{enter}") handleEnterClick();
    else handleCharacterClick(button);
  };

  const handleClearClick = () => {
    if (inputField === "firstName") setFirstName("");
    else if (inputField === "lastName") setLastName("");
    else if (inputField === "MRN") setMRN("");
    else if (inputField === "contactA") setContactA("");
    else if (inputField === "contactB") setContactB("");
  };

  const handleBackspaceClick = () => {
    if (inputField === "firstName") setFirstName(firstName.slice(0, -1));
    else if (inputField === "lastName") setLastName(lastName.slice(0, -1));
    else if (inputField === "MRN") setMRN(MRN.slice(0, -1));
    else if (inputField === "contactA") setContactA(contactA.slice(0, -1));
    else if (inputField === "contactB") setContactB(contactB.slice(0, -1));
  };

  const handleSpaceClick = () => {
    if (inputField === "firstName") setFirstName(firstName + " ");
    else if (inputField === "lastName") setLastName(lastName + " ");
    else if (inputField === "MRN") setMRN(MRN + " ");
    else if (inputField === "contactA") setContactA(contactA + " ");
    else if (inputField === "contactB") setContactB(contactB + " ");
  };

  const handleEnterClick = () => {
    // Handle the enter key press here
  };

  const handleCharacterClick = (button) => {
    if (inputField === "firstName") setFirstName(firstName + button);
    else if (inputField === "lastName") setLastName(lastName + button);
    else if (inputField === "MRN") setMRN(MRN + button);
    else if (inputField === "contactA") setContactA(contactA + button);
    else if (inputField === "contactB") setContactB(contactB + button);
  };

  const [inputField, setInputField] = useState(null);

  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    setSubmitted(true);
  };

  if (submitted) {
    return <App />;
  }

  return (
    <div className="w-screen h-screen bg-slate-950 flex flex-col justify-between items-center">
      <div className="w-[45%] h-[60%] fixed flex flex-col items-center justify-between pt-5">
        <p className="text-slate-200 text-3xl">Enter patient information</p>
        <div className="w-full h-[85%] bg-slate-800 rounded-lg flex flex-col items-center">
          <form
            className="w-full h-full rounded-xl flex flex-col items-start justify-between py-4 px-8"
            onSubmit={handleSubmit}
          >
            <div className="flex w-full justify-start gap-x-[5%]">
              <div className="flex flex-col w-[40%]">
                <label className="text-slate-200 text-xl">First name</label>
                <input
                  onFocus={() => setInputField("firstName")}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2 uppercase"
                  type="text"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value.toUpperCase())}
                  required
                  style={{ caretColor: "white" }}
                />
              </div>
              <div className="flex flex-col w-[40%]">
                <label className="text-slate-200 text-xl">Last name</label>
                <input
                  onFocus={() => setInputField("lastName")}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2 uppercase"
                  type="text"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value.toUpperCase())}
                  required
                  style={{ caretColor: "white" }}
                />
              </div>
              <div className="flex flex-col w-[10%]">
                <label className="text-slate-200 text-xl">Sex</label>
                <select
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2"
                  value={sex}
                  onChange={(e) => setSex(e.target.value)}
                  required
                >
                  <option value=""></option>
                  <option value="M">M</option>
                  <option value="F">F</option>
                </select>
              </div>
            </div>
            <div className="flex w-full justify-start gap-x-[5%]">
              <div className="flex flex-col w-[40%]">
                <label className="text-slate-200 text-xl">Date of birth</label>
                <DatePicker
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2"
                  selected={date}
                  onChange={(date) => setDate(date)}
                  dateFormat="MM/dd/yyyy"
                  maxDate={new Date()}
                  showYearDropdown
                  dropdownMode="select"
                />
              </div>
              <div className="flex flex-col w-[40%]">
                <label className="text-slate-200 text-xl">MRN</label>
                <input
                  onFocus={() => setInputField("MRN")}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2"
                  type="text"
                  value={MRN}
                  onChange={(e) => setMRN(e.target.value)}
                  required
                  style={{ caretColor: "white" }}
                />
              </div>
            </div>
            <div className="flex w-full justify-start gap-x-[5%]">
              <div className="flex flex-col w-[40%]">
                <label className="text-slate-200 text-xl">Contact A</label>
                <input
                  onFocus={() => setInputField("contactA")}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2"
                  type="text"
                  value={contactA}
                  onChange={(e) => setContactA(e.target.value)}
                  required
                  style={{ caretColor: "white" }}
                />
              </div>
              <div className="flex flex-col w-[40%]">
                <label className="text-slate-200 text-xl">Contact B</label>
                <input
                  onFocus={() => setInputField("contactB")}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2"
                  type="text"
                  value={contactB}
                  onChange={(e) => setContactB(e.target.value)}
                  required
                  style={{ caretColor: "white" }}
                />
              </div>
            </div>
            <input
              className="w-[85%] h-9 bg-green-700 rounded-lg text-slate-200 text-xl font-bold"
              type="submit"
              value="Submit"
            />
          </form>
        </div>
      </div>
      <div className="fixed bottom-0 w-full">
        <Keyboard
          onKeyPress={(button) => handleKeyPress(button)}
          layout={{
            default: [
              "1 2 3 4 5 6 7 8 9 0 {bksp}",
              "Q W E R T Y U I O P",
              "A S D F G H J K L",
              "{shift} Z X C V B N M {shift}",
            ],
          }}
          display={{
            "{bksp}": "delete",
            "{shift}": "clear",
            "{space}": "space",
          }}
        />
      </div>
    </div>
  );
};

export default StartPage;
