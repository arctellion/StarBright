
function bundle( keys, elArray ) 
{
   for ( i in elementArray )
   {
      elArray[i].keys = keys;
   }
}

function El( keys, values )  // Element
{
   for ( i in keys )
   {
      if ( values.length >= i && values[i] )
         this[keys[i]] = values[i];
      else
         this[keys[i]] = 0;         
   }
   this.keys = keys;
   return this;
}

function clone( el )
{
	 this.keys = el.keys;
	 for ( i in el.keys )
	    this[keys[i]] = el[keys[i]];

	 return this;
}

function pr( obj, delim, block )
{
   var out = '';
   var keys = obj.keys;
   var list = false;
   for ( i in keys )
   {
      if ( block == 2 )
      {
         var val = keys[i].replace( /\s+$/, '' ).replace( /^\s+/, '' );
         var rval = obj[keys[i]];
         
         if ( val.match( /:$/ ) ) // trailing colon means suppress delimiter
         {
            out += sprintf( val.length, val ) + " " + rval;
         }
         else if ( val.match( /,$/ ) ) // trailing comma means "array context"
         {
            if ( list == false )
            {
               list = true;
               out += " {";
            }
            val = val.replace( /,$/, '' );
            out += sprintf( val.length, val ) + ":"
              + rval + ", ";
         }
         else
         {
            out += sprintf( val.length, val );
            if ( list == true )
            {
               list = false;
               out += ":" + rval + "}";
            }
            else
            {
               out += ": " + rval;
            }
            out += delim;
         }
      }
      else if ( block )
         out += obj[keys[i]] + delim;
      else
         out += sprintf( keys[i].length, obj[keys[i]] ) + delim;
   }
   return out;
}

function prln( obj, delim, block )
{
	return pr( obj, delim, block ) + "\n";
}

function sprintf( pad, value )
{
	 var v2 = '' + value;
	 var out = v2;
	 var text = ( value != parseFloat(value) );
	 
	 if ( v2.length > pad )
	    out = v2.substr( 0, pad );

   for ( var i=0; i<pad - v2.length; i++ )
	    if ( text ) out += ' ';
	    else   	    out = ' ' + out;
	    
   return out;
}

function hdr( keys, delim )
{
   var title = '';
   var sep   = '';
   for ( i in keys )
   {
      title += keys[i] + delim;
      for (var j=0; j<keys[i].length; j++)
         sep += '-';
      sep += delim;
   }
   return title + "\n" + sep + "\n";
}

function compose( elArray )
{
   var out  = clone( elArray[0] );
   for (i=1; i<elArray.length; i++)
   {
      var item = elArray[i];
      for (j in out.keys)
      {
      	 var f1 = '' + item[keys[j]];
      	 
      	 // force a plus sign unless a sigil exists
      	 if ( f1.match( /^[^\(\-\$=x\+\^\_\/]/ ) ) f1 = '+' + f1;
      	 
      	 var field = f1.match( /^([\(\-=x\+\^\_\/]|\$speed x)\s*(.*)$/ );
         var sigil = field[1];
         var val   = field[2];
         
         if ( sigil == '(' )       // ignore string
         {
//            alert( "ignoring " + val );
         }
         else if ( sigil == '=' )  // override
         {
//         	  alert( "overriding " + val );
            out[keys[j]] = val;
         }
         else if ( sigil == 'x' )  // multiply
         {
//         	  alert( "multiplying " + val );
            out[keys[j]] *= parseFloat( val );
            out[keys[j]] = Math.round( out[keys[j]] * 100 ) / 100;
         }
         else if ( sigil == '/' ) // divide
         {
            out[keys[j]] /= parseFloat( val );
            out[keys[j]] = Math.round( out[keys[j]] * 100 ) / 100;         
         }
         else if ( sigil == '-' ) // subtract number
         {
//         	  alert( "subtracting " + val );
         	  out[keys[j]] -= parseInt( val ); // was parseFloat()
         }
         else if ( sigil == '^' ) // take max #
         {
//         	  alert( "max " + val );
            out[keys[j]] = Math.max( parseInt( val ), out[keys[j]] ); // was parseFloat()
         }
         else if ( sigil == '_' ) // take min #
         {
//         	  alert( "min " + val );
         	  out[keys[j]] = Math.min( parseInt( val ), out[keys[j]] ); // was parseFloat()
         }
         else if ( val.match( /\D/ ) ) // concat to front of string
         {
//         	  alert( "concat " + val );
            out[keys[j]] = val + out[keys[j]];
         }
         else if ( sigil == '$speed x' ) // multiply by current speed rating
         {
            var valInt     = out[ 'spd' ] * parseInt( val ); // speed x value
            //out[keys[j]] = parseFloat( out[keys[j]] ) + parseInt(valInt);
            out[keys[j]] = parseInt( out[keys[j]] ) + parseInt(valInt);
         }
         else 
         {
//          if ( keys[j] == 'spd' ) alert( item + ": adding " + parseInt(val) + " to " + keys[j] + " (" + out[keys[j]] + ")" );
            //out[keys[j]] = parseFloat( out[keys[j]] ) + parseInt( val ); // add number
            out[keys[j]] = parseInt( out[keys[j]] ) + parseInt( val ); // add number

//          if ( keys[j] == 'spd' ) alert( keys[j] + ": " + out[keys[j]] );
         }
      }
      //alert( accumulator );
   }
   return out;
}

function printOptions( name, recalc_name, elArray )
{
	 var out = '<select name="' + name + '" onchange="' + recalc_name + '(this.form)">';
	 var keys = elArray[0].keys;
   for ( var i in elArray )
   {
   	  var el = elArray[i];
      out += '<option value="' + el[keys[0]] + '">' + el[keys[1]] + '</option>';
   }
   out += '</select>';
   return out;
}


function mytest()
{
   var keys  = new Array( 'name                              ', 'range', 'price' );
   var itest = new El( keys, new Array( 'foo', 2, 200 ) );
   var ibar  = new El( keys, new Array( '(f20)', 'x1.4', 100 ) );
   
   var out   = compose( new Array( itest, ibar ) );
   return hdr( itest.keys, ' ' )
        + prln( out, ' ', 0 );
}
