
var _Debug = false;  // set this to false to turn debugging off
                     // and get rid of those annoying alert boxes.

// Define exception/error codes
var _NoError = 0;
var _GeneralException = 101;
var _ServerBusy = 102;
var _InvalidArgumentError = 201;
var _ElementCannotHaveChildren = 202;
var _ElementIsNotAnArray = 203;
var _NotInitialized = 301;
var _NotImplementedError = 401;
var _InvalidSetValue = 402;
var _ElementIsReadOnly = 403;
var _ElementIsWriteOnly = 404;
var _IncorrectDataType = 405;


// local variable definitions
var apiHandle = null;
var API = null;
var findAPITries = 0;



/******************************************************************************
**
** Function getSCORMAPI()
** Inputs:  None
** Return:  value contained by APIHandle
**
** Description:
** Returns the handle to API object if it was previously set,
** otherwise it returns null
**
*******************************************************************************/
function getSCORMAPI()
{
   if (apiHandle == null)
   {
      apiHandle = getAPI();	  
   }

   return apiHandle;
}

/*******************************************************************************
**
** Function findAPI(win)
** Inputs:  win - a Window Object
** Return:  If an API object is found, it's returned, otherwise null is returned
**
** Description:
** This function looks for an object named API in parent and opener windows
**
*******************************************************************************/
function findAPI(win)
{
   if (_Debug)
   {
      alert("window to be searched is: "+win.location.href);
   }

   if (win.API != null)
   {
//alert("1  API found == true" + win.name); 
      if (_Debug)
      {
         alert("found API in this window");
      }
	
      return win.API;
   }

   if (win.length > 0)  // does the window have frames?
   { 
      if (_Debug)
      {
         alert("looking for API in window's frames");
      }

      for (var i=0;i<win.length;i++)
      { 

         if (_Debug)
         {
            alert("looking for API in frames["+i+"]");
         }
         var theAPI = findAPI(win.frames[i]);
         if (theAPI != null)
         {
//alert("2  API found == true" + win.name); 		
		return theAPI;
         }
      }
   }

   if (_Debug)
   {
      alert("Didn't find API in this window (or its children).  Returning null from findAPI().");
   }
   return null;

}



/*******************************************************************************
**
** Function getAPI()
** Inputs:  none
** Return:  If an API object is found, it's returned, otherwise null is returned
**
** Description:
** This function looks for an object named API, first in the current window's
** hierarchy, and then, if necessary, in the current window's opener window
** hierarchy (if there is an opener window).
*******************************************************************************/
function getAPI()
{
	
   var API = null; 
	
	//Search all the parents of the current window if there are any
	if ((window.parent != null) && (window.parent != window)) 
	{ 
		
		API = SCORM_ScanParentsForApi(window.parent); 
	} 
	
	if ((API == null) && (window.top.opener != null))
	{ 
		
		API = SCORM_ScanParentsForApi(window.top.opener); 
	} 


   return API;
 }

 function SCORM_ScanParentsForApi(win) 
{ 

	
	
	/*
	Establish an outrageously high maximum number of
	parent windows that we are will to search as a
	safe guard against an infinite loop. This is 
	probably not strictly necessary, but different 
	browsers can do funny things with undefined objects.
	*/
	var MAX_PARENTS_TO_SEARCH = 500; 
	var nParentsSearched = 0;
	
	/*
	Search each parent window until we either:
		 -find the API, 
		 -encounter a window with no parent (parent is null 
				or the same as the current window)
		 -or, have reached our maximum nesting threshold
	*/
	while ( (win.API == null || win.API === undefined) && 
			(win.parent != null) && (win.parent != win) && 
			(nParentsSearched <= MAX_PARENTS_TO_SEARCH) 
		  )
	{ 
				
		nParentsSearched++; 
		win = win.parent;
	} 
	
	/*
	If the API doesn't exist in the window we stopped looping on, 
	then this will return null.
	*/
	return win.API; 
} 

/*******************************************************************************
**
** Function: LMSInitialize()
** Inputs:  None
** Return:  CMIBoolean true if the initialization was successful, or
**          CMIBoolean false if the initialization failed.
**
** Description:
** Initialize communication with LMS by calling the LMSInitialize
** function which will be implemented by the LMS.
**
*******************************************************************************/
function LMSInitialize()
{
   var api = getSCORMAPI();
   if (api == null)
   {
	//if(_Debug){
      alert("Unable to locate the LMS's API Implementation.\nLMSInitialize was not successful.");
	//}
      return "false";
   }

   var result = api.LMSInitialize("");

   if (result.toString() != "true")
   {
      var err = ErrorHandler();
   }

   return result.toString();
}


/*******************************************************************************
**
** Function LMSGetValue(name)
** Inputs:  name - string representing the cmi data model defined category or
**             element (e.g. cmi.core.student_id)
** Return:  The value presently assigned by the LMS to the cmi data model
**       element defined by the element or category identified by the name
**       input value.
**
** Description:
** Wraps the call to the LMS LMSGetValue method
**
*******************************************************************************/
function LMSGetValue(name)
{
   var api = getSCORMAPI();
   if (api == null)
   {
	if(_Debug){
      		alert("Unable to locate the LMS's API Implementation.\nLMSGetValue was not successful.");
	}
      return "";
   }
   else
   {
      var value = api.LMSGetValue(name);
      var errCode = api.LMSGetLastError().toString();
      if (errCode != _NoError)
      {
         // an error was encountered so display the error description
         var errDescription = api.LMSGetErrorString(errCode);
	if(_Debug){
         	alert("LMSGetValue("+name+") failed. \n"+ errDescription);
	}
         return "";
      }
      else
      {
         
         return value.toString();
      }
   }
}

/*******************************************************************************
**
** Function doLMSSetValue(name, value)
** Inputs:  name -string representing the data model defined category or element
**          value -the value that the named element or category will be assigned
** Return:  CMIBoolean true if successful
**          CMIBoolean false if failed.
**
** Description:
** Wraps the call to the LMS LMSSetValue function
**
*******************************************************************************/
function LMSSetValue(name, value)
{
   var api = getSCORMAPI();
   if (api == null)
   {
	if(_Debug){
      		alert("Unable to locate the LMS's API Implementation.\nLMSSetValue was not successful.");
	}
      return;
   }
   else
   {
      var result = api.LMSSetValue(name, value);
      if (result.toString() != "true")
      {
         var err = ErrorHandler();
      }
   }

   return;
}

/*******************************************************************************
**
** Function doLMSCommit()
** Inputs:  None
** Return:  None
**
** Description:
** Call the LMSCommit function 
**
*******************************************************************************/
function LMSCommit()
{
   var api = getSCORMAPI();
   if (api == null)
   {
	if(_Debug){
      		alert("Unable to locate the LMS's API Implementation.\nLMSCommit was not successful.");
	}
      return "false";
   }
   else
   {
      var result = api.LMSCommit("");
      if (result != "true")
      {
         var err = ErrorHandler();
      }
   }

   return result.toString();
}

/*******************************************************************************
**
** Function LMSFinish()
** Inputs:  None
** Return:  CMIBoolean true if successful
**          CMIBoolean false if failed.
**
** Description:
** Close communication with LMS by calling the LMSFinish
** function which will be implemented by the LMS
**
*******************************************************************************/
function LMSFinish()
{
   var api = getSCORMAPI();
   if (api == null)
   {
	if(_Debug){
	      alert("Unable to locate the LMS's API Implementation.\nLMSFinish was not successful.");
	}
      return "false";
   }
   else
   {
      // call the LMSFinish function that should be implemented by the API

      var result = api.LMSFinish("");
      if (result.toString() != "true")
      {
         var err = ErrorHandler();
      }

   }

   return result.toString();
}



/*******************************************************************************
**
** Function doLMSGetLastError()
** Inputs:  None
** Return:  The error code that was set by the last LMS function call
**
** Description:
** Call the LMSGetLastError function 
**
*******************************************************************************/
function LMSGetLastError()
{
   var api = getSCORMAPI();
   if (api == null)
   {
	if(_Debug){
      		alert("Unable to locate the LMS's API Implementation.\nLMSGetLastError was not successful.");
	}
      //since we can't get the error code from the LMS, return a general error
      return _GeneralError;
   }

   return api.LMSGetLastError().toString();
}

/*******************************************************************************
**
** Function doLMSGetErrorString(errorCode)
** Inputs:  errorCode - Error Code
** Return:  The textual description that corresponds to the input error code
**
** Description:
** Call the LMSGetErrorString function 
**
********************************************************************************/
function LMSGetErrorString(errorCode)
{
   var api = getSCORMAPI();
   if (api == null)
   {
	if(_Debug){
      		alert("Unable to locate the LMS's API Implementation.\nLMSGetErrorString was not successful.");
	}
   }

   return api.LMSGetErrorString(errorCode).toString();
}

/*******************************************************************************
**
** Function doLMSGetDiagnostic(errorCode)
** Inputs:  errorCode - Error Code(integer format), or null
** Return:  The vendor specific textual description that corresponds to the 
**          input error code
**
** Description:
** Call the LMSGetDiagnostic function
**
*******************************************************************************/
function LMSGetDiagnostic(errorCode)
{
   var api = getSCORMAPI();
   if (api == null)
   {
	if(_Debug){
      		alert("Unable to locate the LMS's API Implementation.\nLMSGetDiagnostic was not successful.");
	}
   }

   return api.LMSGetDiagnostic(errorCode).toString();
}

/*******************************************************************************
**
** Function LMSIsInitialized()
** Inputs:  none
** Return:  true if the LMS API is currently initialized, otherwise false
**
** Description:
** Determines if the LMS API is currently initialized or not.
**
*******************************************************************************/
function LMSIsInitialized()
{
   // there is no direct method for determining if the LMS API is initialized
   // for example an LMSIsInitialized function defined on the API so we'll try
   // a simple LMSGetValue and trap for the LMS Not Initialized Error

   var api = getSCORMAPI();
   if (api == null)
   {
	if(_Debug){
      		alert("Unable to locate the LMS's API Implementation.\nLMSIsInitialized() failed.");
	}
      return false;
   }
   else
   {
      var value = api.LMSGetValue("cmi.core.student_name");
      var errCode = api.LMSGetLastError().toString();
      if (errCode == _NotInitialized)
      {
         return false;
      }
      else
      {
         return true;
      }
   }
}

/*******************************************************************************
**
** Function ErrorHandler()
** Inputs:  None
** Return:  The current value of the LMS Error Code
**
** Description:
** Determines if an error was encountered by the previous API call
** and if so, displays a message to the user.  If the error code
** has associated text it is also displayed.
**
*******************************************************************************/
function ErrorHandler()
{
   var api = getSCORMAPI();
   if (api == null)
   {
	if(_Debug){
      		alert("Unable to locate the LMS's API Implementation.\nCannot determine LMS error code.");
	}
      return;
   }

   // check for errors caused by or from the LMS
   var errCode = api.LMSGetLastError().toString();
   if (errCode != _NoError)
   {
      // an error was encountered so display the error description
      var errDescription = api.LMSGetErrorString(errCode);

      if (_Debug == true)
      {
         errDescription += "\n";
         errDescription += api.LMSGetDiagnostic(null);
         // by passing null to LMSGetDiagnostic, we get any available diagnostics
         // on the previous error.
      }

	if(_Debug){
      		alert(errDescription);
	}
   }

   return errCode;
}



