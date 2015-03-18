Feature: send sensordata to server

  Scenario: checksum calculation
    Given a data string (a 1234567890 123)(b 1234567891 124)
    When the checksum is being calculated
    Then the result should be 1234567890:1837

  #  Scenario: data transfer on successfull connection
  #  Given
