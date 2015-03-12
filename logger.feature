Feature: store datapoints

  Scenario Outline: store less datapoints then the maximum per file
      Given a maximal amount of <maximal amount> of datapoints per file
      When I log these datapoints: <datapoints>
      Then the total number of logfiles is <t>
      And the file(s) content is: <content>
      And the name of each logfile contains the timestamp of its first datapoint (<content>)
      And the older logfile has been renamed to start with a "C" instead of a T

    Examples: All in one file 
      | maximal amount | datapoints                                              | t | content                                              |
      | 5              | (a 1426083000 1), (b 1426083001 2)                      | 1 | (a 1426083000 1)(b 1426083001 2)                     |
      | 3              | (a 1426083000 12), (a 1426083001 23), (c 1426083002 34) | 1 | (a 1426083000 12)(a 1426083001 23)(c 1426083002 34)  |

    Examples: In two files
      | maximal amount | datapoints                                              | t | content                                                 |
      | 2              | (a 1426083000 12), (a 1426083001 23), (c 1426083002 34) | 2 | (a 1426083000 12)(a 1426083001 23), (c 1426083002 34)   |
      | 1              | (a 1426083000 12), (a 1426083001 23), (c 1426083002 34) | 3 | (a 1426083000 12), (a 1426083001 23), (c 1426083002 34) |
