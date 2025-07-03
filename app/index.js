import { useState } from 'react';
import { View, ScrollView, SafeAreaView, Text, Image, TextInput, TouchableOpacity, StyleSheet, } from 'react-native';
import { Stack } from 'expo-router';
import { images } from '../assets';
import {Picker} from '@react-native-picker/picker';
import Feather from '@expo/vector-icons/Feather';

const Home = () => {
    const [text, setText] = useState('');
    const [keyword, setKeyword] = useState('');
    const [results, setResults] = useState({});
    const [textMode, setTextMode] = useState("1");

    const handleAnalysis = async () => { //send data to flask backend and retrieve
        console.log("Running analysis...");
        try {
            console.log("Sending keywords:", keyword); // Log keywords before sending
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text, keywords: keyword }), // Pass the whole keyword string
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Error:', errorData);
                return;
            }

            const result = await response.json();
            console.log("Received results:", result); // Log the received results
            setResults(result); // Store the results from backend
        } catch (error) {
            console.error('Fetch Error:', error.message);
        }
    };

    const keywordsArray = keyword.split(',').map((kw) => kw.trim());

    return (
        <SafeAreaView>
            <Stack.Screen
                options={{
                    headerStyle: { backgroundColor: '#FFFFFF', height: 80 },
                    headerShadowVisible: false,
                    headerLeft: () => (
                        <View style={{ margin: 30, paddingVertical:10 }}>
                            <Image source={images.logo} style={{ width: 200, height: 80 }} resizeMode='contain' />
                        </View>
                    ),
                    headerTitle: "",
                }}
            />
            <ScrollView contentContainerStyle={styles.container}>
                
                <View style={styles.container2}>
                    {textMode == "1" ? 
                        <TextInput
                            style={styles.textInput}
                            placeholder="Enter text here..."
                            placeholderTextColor="#83829A"
                            value={text}
                            onChangeText={setText}
                            multiline
                        />
                        :
                        <TouchableOpacity style={styles.upload} >
                            <Feather name="upload" size={150} color="#83829A" />
                            <Text style={{fontWeight: "500", color:"#83829A", fontSize: 24, marginTop: 10}}>Upload a .docx file</Text>
                        </TouchableOpacity>

                    }
                    
                    <View>
                        <View style={styles.picker}>
                            <Picker style={{ width: 400, height: 40, borderRadius: 5, textAlign: 'center', color: "#385494"}} selectedValue={textMode} onValueChange={setTextMode}>
                                <Picker.Item label="Enter text" value="1" />
                                <Picker.Item label="Upload docx" value="0" />
                            </Picker>
                        </View>
                        <TextInput
                            style={styles.keywordInput}
                            placeholder="Enter keywords separated by commas here..."
                            placeholderTextColor="#83829A"
                            value={keyword}
                            onChangeText={setKeyword}
                        />
                        <TouchableOpacity
                            style={styles.button}
                            onPress={handleAnalysis}
                        >
                            <Text style={{ color: "#385494", fontWeight: "500" }}> Run analysis </Text>
                        </TouchableOpacity>
                    </View>
                </View>
                {(keyword.trim() === '' ? ['General'] : keywordsArray).map((value, index) => {
                    const result = results[value.toLowerCase()];
                    return (
                        <View style={{ flexDirection: 'row' }} key={index}>
                            <View style={{ textAlign: 'left', width: 1000, marginHorizontal: 10 }}>
                                <Text style={{ color: "#ffffff", fontSize: 36, fontWeight: 'bold', marginTop: 20, marginBottom: 30, marginLeft: 30 }}> {value} - Summary: </Text>
                                <View style={{
                                    height: 600,
                                    borderRadius: 5,
                                    marginBottom: 50,
                                    marginHorizontal: 45,
                                    padding: 10,
                                    width: 900,
                                    textAlignVertical: 'top',
                                    textAlign: 'left',
                                    backgroundColor: "#ccc",
                                }}>
                                    <Text style={{ color: "#83829A", fontSize: 16 }}> {result ? result.relevant_sentences.join(' ') : 'Summary...'}</Text>
                                </View>
                            </View>
                            <View style={{ width: 400, marginHorizontal: 10 }}>
                                <Text style={{ color: "#ffffff", fontSize: 36, fontWeight: 'bold', margin: 10 }}> {value} - Results: </Text>
                                {result && (
                                    <>
                                        <Text style={{ color: "#ffffff", fontSize: 26, margin: 20 }}>Pos: {result.avg_scores ? result.avg_scores.pos.toFixed(3) : '0.000'}</Text>
                                        <Text style={{ color: "#ffffff", fontSize: 26, margin: 20 }}>Neu: {result.avg_scores ? result.avg_scores.neu.toFixed(3) : '0.000'}</Text>
                                        <Text style={{ color: "#ffffff", fontSize: 26, margin: 20 }}>Neg: {result.avg_scores ? result.avg_scores.neg.toFixed(3) : '0.000'}</Text>
                                        <Text style={{ color: "#ffffff", fontSize: 26, margin: 20 }}>Comp: {result.avg_scores ? result.avg_scores.compound.toFixed(3) : '0.000'}</Text>
                                    </>
                                )}
                            </View>
                        </View>
                    );
                })}
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#154197",
        alignItems: 'center',
        justifyContent: 'center',
    },
    container2: {
        flexDirection: 'row',
        paddingTop: 50,
        marginHorizontal: 20
    },
    textInput: {
        height: 600,
        borderRadius: 5,
        marginBottom: 10,
        padding: 10,
        width: 900,
        textAlignVertical: 'top',
        textAlign: 'left',
        marginHorizontal: 10,
        backgroundColor: "#ccc",
    },
    keywordInput: {
        height: 40,
        borderRadius: 5,
        marginBottom: 10,
        padding: 10,
        width: 400,
        marginHorizontal: 10,
        backgroundColor: "#ccc",
    },
    button: {
        flexDirection: "row",
        height: 40,
        width: 400,
        backgroundColor: '#ffffff',
        borderRadius: 5,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 20,
        marginHorizontal: 10,
        marginVertical: 10
    },
    picker: {
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 10,
        marginRight: 10,
        marginBottom: 20,
        flexDirection: "row",
    },
    upload: {
        backgroundColor:"#CCC",
        width: 900,
        height: 600,
        borderRadius: 5,
        justifyContent: "center",
        alignItems: "center",
        marginBottom: 10,
        alignSelf:"center",
        padding: 10,
        marginHorizontal: 10,
    }
});

export default Home;