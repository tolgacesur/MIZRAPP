import React from 'react';
import {  View,StyleSheet,ScrollView,Image,TouchableHighlight, FlatList, Text } from 'react-native';
import {HttpService} from '../../services/HttpService';

class Products extends React.Component {

	constructor(props){
			super(props);
			this.state={
				products : []
			}
	}

	componentWillMount() {
		const subCategoryId = this.props.navigation.state.params.subCategoryId
		HttpService().get(`http://localhost/api/products/${subCategoryId}`).then(function(res){
			this.setState({
				products : res.data.products,
			});
		}.bind(this));
	}

	_keyExtractor = (item, index) => item._id;

	_renderItem = ({item}) => (
		<TouchableHighlight onPress={() =>  this.props.navigation.navigate('repriceScreen',{product:item})}>
			{/* <Image
          style={{width: 400, height: 200}}
          source={{uri: 'https://cdn.pixabay.com/photo/2015/05/02/08/02/angel-749625__340.jpg'}}
        /> */}
        <View style={{flex:1,flexDirection:'row',justifyContent:'flex-start', alignItems:'center', height:50}}>
			<Text style={{paddingLeft:5,fontFamily:'tipopepel', marginLeft:35, fontSize:15, color:'#7FDF60'}}>{item.name} {item.desc} {item.price}</Text>
        </View>
    </TouchableHighlight>
	);

 render() {
    const { navigate } = this.props.navigation;
     return(
      <View style={{}}>
       <FlatList
				data={this.state.products}
				keyExtractor={this._keyExtractor}
        renderItem={this._renderItem}
      	/>
      </View>
     )
 }
}

export default Products