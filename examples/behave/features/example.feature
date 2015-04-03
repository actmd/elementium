Feature: Behave with Elementium

  Scenario: Show that we can run behave with elementium
     Given we can access the Google page
      when we enter something in the search box
      then we see search results
