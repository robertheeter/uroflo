import axios from "axios";
import { useState, useEffect } from "react";
import { useSpring, animated } from "react-spring";
import { SettingsIcon } from "@chakra-ui/icons";
import {
  ChakraProvider,
  Progress,
  Flex,
  Box,
  Text,
  Spacer,
  Image,
  Switch,
  Divider,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
} from "@chakra-ui/react";

function App() {
  axios.defaults.baseURL = "http://localhost:8000"; // proxy

  const [hematuria_level, setHematuriaLevel] = useState(0); // integer; outflow hematuria level/severity
  // const [hematuria_color, setHematuriaColor] = useState([]); // outflow 0-255 [R, G, B] color

  const [supply_volume, setSupplyVolume] = useState(0); // float (L); supply bag volume
  const [supply_rate, setSupplyRate] = useState(0); // float (mL/min); supply bag flow rate
  const [supply_percent, setSupplyPercent] = useState(0); // float (%); percent supply bag full
  // const [supply_time, setSupplyTime] = useState(0); // integer (s); time to supply bag empty

  // const [waste_volume, setWasteVolume] = useState(0); // float (L); waste bag volume
  // const [waste_rate, setWasteRate] = useState(0); // float (mL/min); waste bag flow rate
  // const [waste_percent, setWastePercent] = useState(0); // float (%); percent waste bag full
  // const [waste_time, setWasteTime] = useState(0);  // integer (s); time to waste bag full

  // const [occlusion_level, setOcclusionLevel] = useState(0); // integer; peristaltic pump or tube compression occlusion level

  // const [device_status, setDeviceStatus] = useState(0); // integer; CBI notification status
  // const [device_mode, setDeviceMode] = useState(0); // boolean; automatic or manual device control mode

  // const [patient_first_name, setPatientFirstName] = useState(0); // string; patient first name
  // const [patient_middle_name, setPatientMiddleName] = useState(0); // string; patient middle name
  // const [patient_last_name, setPatientLastName] = useState(0); // string; patient last name
  // const [patient_id, setPatientId] = useState(0); // string; patient ID
  // const [patient_birth_date, setPatientBirthDate] = useState(0); // date; patient date of birth

  // const [doctor_first_name, setDoctorFirstName] = useState(0); // string; doctor first name
  // const [doctor_middle_name, setDoctorMiddleName] = useState(0); // string; doctor middle name
  // const [doctor_last_name, setDoctorLastName] = useState(0); // string; doctor last name
  // const [doctor_id, setDoctorId] = useState(0); // string; doctor ID

  // const [duration_time, setDurationTime] = useState(0); // integer (min); duration on CBI

  const [isSwitchOn, setSwitchOn] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const AnimatedSettingsIcon = animated(SettingsIcon);

  const springProps = useSpring({
    from: { rotation: 0 },
    to: { rotation: isSwitchOn ? 360 : 0 },
    loop: isSwitchOn,
    reset: !isSwitchOn,
    config: { duration: 2000 },
  });

  const [time, setTime] = useState(
    new Date().toLocaleString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      month: "2-digit",
      day: "2-digit",
      year: "numeric",
      hour12: true,
    })
  );

  useEffect(() => {
    let interval;
    let startTime = 0;

    if (isSwitchOn) {
      startTime = Date.now();
      interval = setInterval(() => {
        setElapsedTime(Math.floor((Date.now() - startTime) / 1000));
      }, 1000);
    } else {
      setElapsedTime(0);
    }

    return () => clearInterval(interval);
  }, [isSwitchOn]);

  useEffect(() => {
    let interval;

    if (isSwitchOn) {
      interval = setInterval(() => {
        axios
          .get("http://localhost:8000/user_interface/get_hematuria")
          .then((response) => {
            setHematuriaLevel(response.data.level);
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
      }, 10000);
    }

    return () => clearInterval(interval);
  }, [isSwitchOn]);

  useEffect(() => {
    let interval;

    if (isSwitchOn) {
      interval = setInterval(() => {
        axios
          .get("http://localhost:8000/user_interface/get_supply")
          .then((response) => {
            setSupplyVolume(response.data.volume);
            setSupplyRate(response.data.rate);
            setSupplyPercent(response.data.percent);
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
      }, 10000);
    }

    return () => clearInterval(interval);
  }, [isSwitchOn]);

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(
        new Date().toLocaleString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
          month: "2-digit",
          day: "2-digit",
          year: "numeric",
          hour12: true,
        })
      );
    }, 1000);

    return () => {
      clearInterval(timer);
    };
  }, []);

  const getColor = (value) => {
    if (value <= 20) {
      return "#ddc588";
    } else if (value <= 40) {
      return "#cf8f70";
    } else if (value <= 60) {
      return "#a8372a";
    } else if (value <= 80) {
      return "#811e1b";
    } else {
      return "#491210";
    }
  };

  function formatTime(seconds) {
    if (seconds < 60) {
      return `${seconds}s`;
    } else if (seconds < 3600) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes}m ${remainingSeconds}s`;
    } else {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const remainingSeconds = seconds % 60;
      return `${hours}h ${minutes}m ${remainingSeconds}s`;
    }
  }

  return (
    <ChakraProvider>
      <Flex direction="column" h="100vh">
        <Flex
          as="header"
          width="100%"
          padding="3"
          boxShadow="md"
          justifyContent="space-between"
          alignItems="center"
        >
          <Flex direction="row" align="center" gap="6">
            <Image
              src="uroflo_logo_full.png"
              alt="Description of the image"
              boxSize="100px"
              objectFit="contain"
            />

            <Flex direction="column" align="center" gap="3">
              <AnimatedSettingsIcon
                boxSize={9}
                style={{
                  transform: springProps.rotation.to((r) => `rotate(${r}deg)`),
                }}
              />

              <Switch
                size="lg"
                isChecked={isSwitchOn}
                onChange={(e) => setSwitchOn(e.target.checked)}
                colorScheme="green"
              />
            </Flex>

            <Stat>
              <StatLabel fontSize="lg">Time on CBI:</StatLabel>
              <StatNumber fontSize="2xl">{formatTime(elapsedTime)}</StatNumber>
              <StatHelpText fontSize="md">Dr. Sagar Patel</StatHelpText>
            </Stat>
          </Flex>

          <Text fontSize="2xl" fontWeight="bold">
            {time}
          </Text>
        </Flex>

        <Flex direction="row" h="100vh">
          <Flex direction="column" flex="1" align="center" justify="center">
            <Text fontSize="5xl" fontWeight="bold" marginTop="3">
              Doe, John
            </Text>
            <Text fontSize="xl" fontWeight="bold" marginTop="3">
              Patient ID: 123456789
            </Text>
            <Text fontSize="xl" fontWeight="bold" marginTop="3">
              DOB: 01/01/1990
            </Text>
          </Flex>

          <Flex
            direction="column"
            align="center"
            justify="center"
            height="100%"
          >
            <Divider
              orientation="vertical"
              height="90%"
              borderWidth="1.25px"
              borderColor="gray.300"
            />
          </Flex>

          <Flex direction="column" flex="3">
            <Flex direction="column" justify="center" align="center" flex="1">
              <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                textAlign="center"
                width="75%"
                borderRadius="30px"
                padding="6"
                background="#fceded"
              >
                <Text fontSize="3xl" fontWeight="bold" marginBottom="1">
                  Hematuria
                </Text>

                <Box marginBottom="4">
                  <Text fontSize="2xl">{hematuria_level}%</Text>
                </Box>

                <Spacer />

                <Progress
                  value={hematuria_level}
                  width="80%"
                  borderRadius="full"
                  bgColor="white"
                  sx={{
                    div: {
                      backgroundColor: getColor(hematuria_level),
                    },
                    "& > div:first-child": {
                      transitionProperty: "width",
                    },
                  }}
                />
              </Box>
            </Flex>

            <Flex direction="column" justify="center" align="center" flex="1">
              <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                textAlign="center"
                width="75%"
                borderRadius="30px"
                padding="6"
                background="#e1effa"
              >
                <Text fontSize="3xl" fontWeight="bold" marginBottom="1">
                  Supply Bag
                </Text>

                <Box marginBottom="4">
                  <Text fontSize="2xl">{supply_volume} L</Text>
                  <Text fontSize="2xl">{supply_percent}% Left</Text>
                </Box>

                <Spacer />

                <Progress
                  value={supply_percent}
                  width="80%"
                  borderRadius="full"
                  bgColor="white"
                  colorScheme="blue"
                  sx={{
                    "& > div:first-child": {
                      transitionProperty: "width",
                    },
                  }}
                />
              </Box>
            </Flex>

            <Flex direction="column" justify="center" align="center" flex="1">
              <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                textAlign="center"
                width="75%"
                borderRadius="30px"
                padding="6"
                background="#daf5ea"
              >
                <Text fontSize="3xl" fontWeight="bold" marginBottom="1">
                  Inflow Rate
                </Text>

                <Box marginBottom="4">
                  <Text fontSize="2xl">{supply_rate} mL/min</Text>
                </Box>

                <Spacer />

                <Progress
                  value={supply_rate}
                  width="80%"
                  borderRadius="full"
                  bgColor="white"
                  colorScheme="green"
                  sx={{
                    "& > div:first-child": {
                      transitionProperty: "width",
                    },
                  }}
                />
              </Box>
            </Flex>
          </Flex>
        </Flex>
      </Flex>
    </ChakraProvider>
  );
}

export default App;
