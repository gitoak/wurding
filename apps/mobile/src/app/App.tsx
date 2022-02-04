/* eslint-disable jsx-a11y/accessible-emoji */
import React, {useRef, useState} from 'react';
import {Button, ScrollView, StyleSheet, View,} from 'react-native';

// @ts-ignore
import openURLInBrowser from 'react-native/Libraries/Core/Devtools/openURLInBrowser';

const App = () => {
  const [whatsNextYCoord, setWhatsNextYCoord] = useState<number>(0);
  const scrollViewRef = useRef<null | ScrollView>(null);

  return (
    <>
      <View style={styles.container}>
        <Button title={'Open in browser'} onPress={(e) => console.log(e)}/>
      </View>
    </>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default App;
