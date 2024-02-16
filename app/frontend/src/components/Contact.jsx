import UroFloLogo from "../assets/uroflo_blue_name_cropped.svg";

const Contact = () => {
  return (
    <div className="h-full w-full flex flex-col justify-end items-end text-xl gap-y-2">
      <img src={UroFloLogo} alt="Description of Image" className="w-[65%]" />
      <div className="text-xl flex flex-col items-end">
        <p>02/12/2024 09:12</p>
      </div>
    </div>
  );
};

export default Contact;
