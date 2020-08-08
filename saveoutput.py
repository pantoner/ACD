from contextlib import suppress
import pickle

def savepickle(listoflist):

	aup1name = "";aup2name ="";aup3name=""; aup4name = "";aup5name ="";aup6name="" 
	with suppress(IndexError):aup1name = listoflist[0][0][6:11].strip() #[6:11]
	pickle.dump(aup1name, open( "pfiles/aup1.p", "wb" ) )
	with suppress(IndexError):aup2name = listoflist[0][1][6:11].strip() #[6:11]
	pickle.dump(aup2name, open( "pfiles/aup2.p", "wb" ) )
	with suppress(IndexError):aup3name = listoflist[0][2][6:11].strip() #[6:11]
	pickle.dump(aup3name, open( "pfiles/aup3.p", "wb" ) )
	with suppress(IndexError):aup4name = listoflist[0][3][6:11].strip() #[6:11]
	pickle.dump(aup4name, open( "pfiles/aup4.p", "wb" ) )
	with suppress(IndexError):aup5name = listoflist[0][4][6:11].strip() #[6:11]
	pickle.dump(aup5name, open( "pfiles/aup5.p", "wb" ) )
	with suppress(IndexError):aup6name = listoflist[0][5][6:11].strip() #[6:11]
	pickle.dump(aup6name, open( "pfiles/aup6.p", "wb" ) )

	cup1name = "";cup2name ="";cup3name="" 
	with suppress(IndexError):cup1name = listoflist[4][0][6:11].strip() #[6:11]
	pickle.dump(cup1name, open( "pfiles/cup1.p", "wb" ) )
	with suppress(IndexError):cup2name = listoflist[4][1][6:11].strip() #[6:11]
	pickle.dump(cup2name, open( "pfiles/cup2.p", "wb" ) )
	with suppress(IndexError):cup3name = listoflist[4][2][6:11].strip() #[6:11]
	pickle.dump(cup3name, open( "pfiles/cup3.p", "wb" ) )

	adwn1name = "";adwn2name ="";adwn3name=""; adwn4name = "";adwn5name ="";adwn6name="" 
	with suppress(IndexError):adwn1name = listoflist[1][0][6:11].strip() #[6:11]
	pickle.dump(adwn1name, open( "pfiles/adwn1.p", "wb" ) )
	with suppress(IndexError):adwn2name = listoflist[1][1][6:11].strip() #[6:11]
	pickle.dump(adwn2name, open( "pfiles/adwn2.p", "wb" ) )
	with suppress(IndexError):adwn3name = listoflist[1][2][6:11].strip() #[6:11]
	pickle.dump(adwn3name, open( "pfiles/adwn3.p", "wb" ) )
	with suppress(IndexError):adwn4name = listoflist[1][3][6:11].strip() #[6:11]
	pickle.dump(adwn4name, open( "pfiles/adwn4.p", "wb" ) )
	with suppress(IndexError):adwn5name = listoflist[1][4][6:11].strip() #[6:11]
	pickle.dump(adwn5name, open( "pfiles/adwn5.p", "wb" ) )
	with suppress(IndexError):adwn6name = listoflist[1][5][6:11].strip() #[6:11]
	pickle.dump(adwn6name, open( "pfiles/adwn6.p", "wb" ) )

	adwnfail1name = "";adwnfail2name ="";adwnfail3name=""; adwnfail4name = "";adwnfail5name ="";adwnfail6name="" 
	with suppress(IndexError):adwnfail1name = listoflist[2][0][6:11].strip() #[6:11]
	pickle.dump(adwnfail1name, open( "pfiles/adwnfail1.p", "wb" ) )
	with suppress(IndexError):adwnfail2name = listoflist[2][1][6:11].strip() #[6:11]
	pickle.dump(adwnfail2name, open( "pfiles/adwnfail2.p", "wb" ) )
	with suppress(IndexError):adwnfail3name = listoflist[2][2][6:11].strip() #[6:11]
	pickle.dump(adwnfail3name, open( "pfiles/adwnfail3.p", "wb" ) )
	with suppress(IndexError):adwnfail4name = listoflist[2][3][6:11].strip() #[6:11]
	pickle.dump(adwnfail4name, open( "pfiles/adwnfail4.p", "wb" ) )
	with suppress(IndexError):adwnfail5name = listoflist[2][4][6:11].strip() #[6:11]
	pickle.dump(adwnfail5name, open( "pfiles/adwnfail5.p", "wb" ) )
	with suppress(IndexError):adwnfail6name = listoflist[2][5][6:11].strip() #[6:11]
	pickle.dump(adwnfail6name, open( "pfiles/adwnfail6.p", "wb" ) )
	
	cdwn1name = "";cdwn2name ="";cdwn3name="" 
	with suppress(IndexError):cdwn1name = listoflist[5][0][6:11].strip() #[6:11]
	pickle.dump(cdwn1name, open( "pfiles/cdwn1.p", "wb" ) )
	with suppress(IndexError):cdwn2name = listoflist[5][1][6:11].strip() #[6:11]
	pickle.dump(cdwn2name, open( "pfiles/cdwn2.p", "wb" ) )
	with suppress(IndexError):cdwn3name = listoflist[5][2][6:11].strip() #[6:11]
	pickle.dump(cdwn3name, open( "pfiles/cdwn3.p", "wb" ) )

	aupfail1name = "";aupfail2name ="";aupfail3name=""; aupfail4name = "";aupfail5name ="";aupfail6name="" 
	with suppress(IndexError):aupfail1name = listoflist[3][0][6:11].strip() #[6:11]
	pickle.dump(aupfail1name, open( "pfiles/aupfail1.p", "wb" ) )
	with suppress(IndexError):aupfail2name = listoflist[3][1][6:11].strip() #[6:11]
	pickle.dump(aupfail2name, open( "pfiles/aupfail2.p", "wb" ) )
	with suppress(IndexError):aupfail3name = listoflist[3][2][6:11].strip() #[6:11]
	pickle.dump(aupfail3name, open( "pfiles/aupfail3.p", "wb" ) )
	with suppress(IndexError):aupfail4name = listoflist[3][3][6:11].strip() #[6:11]
	pickle.dump(aupfail4name, open( "pfiles/aupfail4.p", "wb" ) )
	with suppress(IndexError):aupfail5name = listoflist[3][4][6:11].strip() #[6:11]
	pickle.dump(aupfail5name, open( "pfiles/aupfail5.p", "wb" ) )
	with suppress(IndexError):aupfail6name = listoflist[3][5][6:11].strip() #[6:11]
	pickle.dump(aupfail6name, open( "pfiles/aupfail6.p", "wb" ) )


