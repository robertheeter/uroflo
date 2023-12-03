import axios from "axios";
import { useState, useEffect } from "react";
import {
  ChakraProvider,
  Progress,
  Flex,
  Box,
  Text,
  Spacer,
  Image,
} from "@chakra-ui/react";

function App() {
  const [hematuria, setHematuria] = useState(0);
  setHematuria(420)
  const [saline, setSaline] = useState(0);
  const [salinepercent, setSalinePercent] = useState(0);
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
    const interval = setInterval(() => {
      // setHematuria(2);
      axios.get("http://localhost:8000/user_interface/get_hematuria")
        .then(response => {
          console.log(response.data.value)
          // setHematuria(44444);
          setHematuria(response.data.value);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      axios.get("http://localhost:8000/user_interface/get_saline_weight")
        .then(response => {
          console.log(response.data.volume)
          console.log(response.data.percentage)
          setSaline(3);
          setSalinePercent(9);
          // setSaline([...response.data.volume]);
          // setSalinePercent([...response.data.percentage]);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

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

  return (
    <ChakraProvider>
      <Flex direction="column" h="100vh">
        <Flex
          as="header"
          width="100%"
          padding="1rem"
          boxShadow="md"
          justifyContent="space-between"
          alignItems="center"
        >
          <Image
            src="uroflo_logo_full.png"
            alt="Description of the image"
            boxSize="100px"
            objectFit="contain"
          />
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
                  Hematuria Degree
                </Text>

                <Box marginBottom="4">
                  <Text fontSize="2xl">{hematuria}%</Text>
                </Box>

                <Spacer />

                <Progress
                  value={hematuria}
                  width="80%"
                  borderRadius="full"
                  bgColor="white"
                  sx={{
                    div: {
                      backgroundColor: getColor(hematuria),
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
                  Saline Weight
                </Text>

                <Box marginBottom="4">
                  <Text fontSize="2xl">{saline} L</Text>
                  <Text fontSize="2xl">{salinepercent}% Left</Text>
                </Box>

                <Spacer />

                <Progress
                  value={saline}
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
          </Flex>
        </Flex>
      </Flex>
    </ChakraProvider>
  );
}

export default App;
