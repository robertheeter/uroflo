import App from "../App";
import { useState } from "react";
import DatePicker from "react-datepicker";
import Keyboard from "react-simple-keyboard";
import "react-dropdown/style.css";
import "react-datepicker/dist/react-datepicker.css";
import "react-simple-keyboard/build/css/index.css";
// import InputMask from "react-input-mask";

const StartPage = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [sex, setSex] = useState("");
  const [date, setDate] = useState(null);
  const [mrn, setMRN] = useState("");
  const [contactA, setContactA] = useState("");
  const [contactB, setContactB] = useState("");
  const [inputField, setInputField] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [isKeyboardVisible, setIsKeyboardVisible] = useState(false);

  const handleKeyPress = (button) => {
    if (button === "{enter}") setIsKeyboardVisible(false); // Hide the keyboard
    else if (button === "{shift}") handleClearClick();
    else if (button === "{bksp}") handleBackspaceClick();
    else if (button === "{space}") handleSpaceClick();
    else handleCharacterClick(button);
  };

  const handleClearClick = () => {
    if (inputField === "firstName") setFirstName("");
    else if (inputField === "lastName") setLastName("");
    else if (inputField === "mrn") setMRN("");
    else if (inputField === "contactA") setContactA("");
    else if (inputField === "contactB") setContactB("");
  };

  const handleBackspaceClick = () => {
    if (inputField === "firstName") setFirstName(firstName.slice(0, -1));
    else if (inputField === "lastName") setLastName(lastName.slice(0, -1));
    else if (inputField === "mrn") setMRN(mrn.slice(0, -1));
    else if (inputField === "contactA") setContactA(contactA.slice(0, -1));
    else if (inputField === "contactB") setContactB(contactB.slice(0, -1));
  };

  const handleSpaceClick = () => {
    if (inputField === "firstName") setFirstName(firstName + " ");
    else if (inputField === "lastName") setLastName(lastName + " ");
    else if (inputField === "mrn") setMRN(mrn + " ");
    else if (inputField === "contactA") setContactA(contactA + " ");
    else if (inputField === "contactB") setContactB(contactB + " ");
  };

  const handleCharacterClick = (button) => {
    if (inputField === "firstName")
      setFirstName((prevValue) => prevValue + button.toUpperCase());
    else if (inputField === "lastName")
      setLastName((prevValue) => prevValue + button.toUpperCase());
    else if (inputField === "mrn") setMRN((prevValue) => prevValue + button);
    else if (inputField === "contactA")
      setContactA((prevValue) => prevValue + button);
    else if (inputField === "contactB")
      setContactB((prevValue) => prevValue + button);
  };

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
                  onFocus={() => {
                    setInputField("firstName");
                    setIsKeyboardVisible(true); // Show the keyboard
                  }}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2 uppercase"
                  type="text"
                  value={firstName}
                  required
                  style={{ caretColor: "white" }}
                />
              </div>
              <div className="flex flex-col w-[40%]">
                <label className="text-slate-200 text-xl">Last name</label>
                <input
                  onFocus={() => {
                    setInputField("lastName");
                    setIsKeyboardVisible(true); // Show the keyboard
                  }}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2 uppercase"
                  type="text"
                  value={lastName}
                  required
                  style={{ caretColor: "white" }}
                />
              </div>
              <div className="flex flex-col w-[10%]">
                <label className="text-slate-200 text-xl">Sex</label>
                <select
                  onFocus={() => {
                    setIsKeyboardVisible(false); // hide the keyboard
                  }}
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
                  onFocus={() => {
                    setIsKeyboardVisible(false); // hide the keyboard
                  }}
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
                  onFocus={() => {
                    setInputField("mrn");
                    setIsKeyboardVisible(true); // Show the keyboard
                  }}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2 uppercase"
                  type="text"
                  value={mrn}
                  required
                  style={{ caretColor: "white" }}
                />
              </div>
            </div>
            <div className="flex w-full justify-start gap-x-[5%]">
              <div className="flex flex-col w-[40%]">
                <label className="text-slate-200 text-xl">Contact A</label>
                <input
                  onFocus={() => {
                    setInputField("contactA");
                    setIsKeyboardVisible(true); // Show the keyboard
                  }}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2 uppercase"
                  type="text"
                  value={contactA}
                  required
                  style={{ caretColor: "white" }}
                />
              </div>
              <div className="flex flex-col w-[40%]">
                <label className="text-slate-200 text-xl">Contact B</label>
                <input
                  onFocus={() => {
                    setInputField("contactB");
                    setIsKeyboardVisible(true); // Show the keyboard
                  }}
                  className="border-2 mt-2 border-slate-200 bg-slate-950 rounded-lg w-full h-9 text-xl text-slate-200 px-2 uppercase"
                  type="text"
                  value={contactB}
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
      <div className="fixed bottom-0 w-full ">
        {isKeyboardVisible && (
          <Keyboard
            theme={"hg-theme-default"}
            onKeyPress={(button) => handleKeyPress(button)}
            layout={{
              default: [
                "1 2 3 4 5 6 7 8 9 0 {bksp}",
                "Q W E R T Y U I O P",
                "A S D F G H J K L",
                "{shift} Z X C V B N M {enter}",
              ],
            }}
            display={{
              "{bksp}": "delete",
              "{shift}": "clear",
              "{enter}": "enter",
            }}
            buttonTheme={[
              {
                class: "text-3xl text-slate-950",
                buttons:
                  "{bksp} {shift} {enter} 1 2 3 4 5 6 7 8 9 0 Q W E R T Y U I O P A S D F G H J K L Z X C V B N M",
              },
              {
                class: "font-bold",
                buttons: "{bksp} {shift} {enter}",
              },
            ]}
          />
        )}
      </div>
    </div>
  );
};

export default StartPage;
