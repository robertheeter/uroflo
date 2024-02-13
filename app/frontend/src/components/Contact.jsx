const Contact = () => {
  return (
    <div className="h-full w-full flex flex-col justify-between text-xl text-slate-200">
      <div className="flex flex-col justify-center">
        <p>CONTACT 1: (012)-345-6789</p>
        <p>CONTACT 2: (123)-456-7890</p>
      </div>

      <div className="rounded-lg bg-red-300 flex w-[55%] justify-center items-center text-slate-950 font-bold px-3 py-1">
        RESET DEVICE
      </div>
    </div>
  );
};

export default Contact;
