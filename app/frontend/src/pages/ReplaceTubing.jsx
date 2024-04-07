import axios from "axios";
import { useNavigate, useLocation } from "react-router-dom";
import { FaArrowLeftLong } from "react-icons/fa6";

const ReplaceTubing = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const resetInitiated = location.state?.resetInitiated;

  const back = () => {
    navigate("/replace/waste/step3", { state: { resetInitiated } });
  };

  const done = () => {
    const url = "http://localhost:8000/interface/setup";
    const data = {
      setup: "TRUE",
    };
    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    navigate("/home");
  };

  const click = () => {
    const url = "http://localhost:8000/interface/click";
    const data = {
      click: "TRUE",
    };
    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="w-screen h-screen bg-slate-950 flex flex-col justify-center items-center">
      <div className="w-[50%] h-[60%] bg-slate-800 rounded-2xl flex flex-col justify-between items-center pt-16 pb-10">
        <h1 className="text-5xl text-slate-200 font-bold">Replace tubing</h1>
        <div className="w-full flex flex-row justify-end items-center px-10">
          {/* <button
            className="bg-slate-800 border-slate-200 border-2 w-40 h-20 rounded-lg flex justify-center items-center"
            onClick={back}
          >
            <FaArrowLeftLong className="text-6xl text-slate-200" />
          </button> */}
          <button
            className="bg-green-600 w-full h-20 rounded-lg flex justify-center items-center text-3xl text-slate-200"
            onClick={done}
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReplaceTubing;
