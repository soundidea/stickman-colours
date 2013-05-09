'''
These functions are adapted from the pseudocode formulae at:
http://www.easyrgb.com/index.php?X=MATH
'''

def rgb_2_hsl(R, G, B):
	var_R = ( R / 255.0 )
	var_G = ( G / 255.0 )
	var_B = ( B / 255.0 )

	var_Min = min( var_R, var_G, var_B )
	var_Max = max( var_R, var_G, var_B )
	del_Max = var_Max - var_Min

	L = ( var_Max + var_Min ) / 2.0

	if del_Max == 0:
		H = 0
		S = 0
	else:
		if L < 0.5:
			S = del_Max / ( var_Max + var_Min )
		else:
			S = del_Max / ( 2.0 - var_Max - var_Min )

		del_R = ( ( ( var_Max - var_R ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
		del_G = ( ( ( var_Max - var_G ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
		del_B = ( ( ( var_Max - var_B ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max

		if var_R == var_Max:
			H = del_B - del_G
		elif var_G == var_Max:
			H = ( 1.0 / 3.0 ) + del_R - del_B
		elif var_B == var_Max:
			H = ( 2.0 / 3.0 ) + del_G - del_R

		if H < 0:
			H += 1
		if H > 1:
			H -= 1
	return (H, S, L)

def rgb_2_hsv(R, G, B):
	var_R = ( R / 255.0 )
	var_G = ( G / 255.0 )
	var_B = ( B / 255.0 )

	var_Min = min( var_R, var_G, var_B )
	var_Max = max( var_R, var_G, var_B )
	del_Max = var_Max - var_Min

	V = var_Max

	if del_Max == 0:
		H = 0
		S = 0
	else:
		S = del_Max / var_Max

		del_R = ( ( ( var_Max - var_R ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
		del_G = ( ( ( var_Max - var_G ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
		del_B = ( ( ( var_Max - var_B ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max

		if var_R == var_Max:
			H = del_B - del_G
		elif var_G == var_Max:
			H = ( 1.0 / 3.0 ) + del_R - del_B
		elif var_B == var_Max:
			H = ( 2.0 / 3.0 ) + del_G - del_R

		if H < 0:
			H += 1
		if H > 1:
			H -= 1
	return (H, S, V)

def rgb_2_xyz(R, G, B):
	var_R = ( R / 255.0 )
	var_G = ( G / 255.0 )
	var_B = ( B / 255.0 )

	if var_R > 0.04045:
		var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
	else:
		var_R = var_R / 12.92
	if var_G > 0.04045:
		var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
	else:
		var_G = var_G / 12.92
	if var_B > 0.04045:
		var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
	else:
		var_B = var_B / 12.92

	var_R = var_R * 100.0
	var_G = var_G * 100.0
	var_B = var_B * 100.0

	X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
	Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
	Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505
	return (X, Y, Z)

def xyz_2_hunterlab(X, Y, Z):
	rootY = Y ** (1.0 / 2.0)
	L = 10.0 * rootY
	a = 17.5 * ( ( ( 1.02 * X ) - Y ) / rootY )
	b = 7.0 * ( ( Y - ( 0.847 * Z ) ) / rootY )
	return (L, a, b)

def xyz_2_cielab(X, Y, Z):
	var_X = X / 95.047
	var_Y = Y / 100.0
	var_Z = Z / 108.883

	if var_X > 0.008856:
		var_X = var_X ** ( 1.0 / 3.0 )
	else:
		var_X = ( 7.787 * var_X ) + ( 16.0 / 116.0 )
	if var_Y > 0.008856:
		var_Y = var_Y ** ( 1.0 / 3.0 )
	else:
		var_Y = ( 7.787 * var_Y ) + ( 16.0 / 116.0 )
	if var_Z > 0.008856:
		var_Z = var_Z ** ( 1.0 / 3.0 )
	else:
		var_Z = ( 7.787 * var_Z ) + ( 16.0 / 116.0 )

	L = ( 116.0 * var_Y ) - 16.0
	a = 500.0 * ( var_X - var_Y )
	b = 200.0 * ( var_Y - var_Z )
	return (L, a, b)

def xyz_2_cieluv(X, Y, Z):
	var_U = ( 4.0 * X ) / ( X + ( 15.0 * Y ) + ( 3.0 * Z ) )
	var_V = ( 9.0 * Y ) / ( X + ( 15.0 * Y ) + ( 3.0 * Z ) )

	var_Y = Y / 100.0
	if var_Y > 0.008856:
		var_Y = var_Y ** ( 1.0 / 3.0 )
	else:
		var_Y = ( 7.787 * var_Y ) + ( 16.0 / 116.0 )

	ref_X =  95.047
	ref_Y = 100.000
	ref_Z = 108.883

	ref_U = ( 4.0 * ref_X ) / ( ref_X + ( 15.0 * ref_Y ) + ( 3.0 * ref_Z ) )
	ref_V = ( 9.0 * ref_Y ) / ( ref_X + ( 15.0 * ref_Y ) + ( 3.0 * ref_Z ) )

	L = ( 116.0 * var_Y ) - 16.0
	u = 13.0 * L * ( var_U - ref_U )
	v = 13.0 * L * ( var_V - ref_V )
	return (L, u, v)

def cielab_2_xyz(L, a, b):
	var_Y = ( L + 16.0 ) / 116.0
	var_X = a / 500.0 + var_Y
	var_Z = var_Y - b / 200.0

	if var_Y ** 3.0 > 0.008856:
		var_Y = var_Y ** 3.0
	else:
		var_Y = ( var_Y - 16.0 / 116.0 ) / 7.787
	if var_X ** 3.0 > 0.008856:
		var_X = var_X ** 3.0
	else:
		var_X = ( var_X - 16.0 / 116.0 ) / 7.787
	if var_Z ** 3 > 0.008856:
		var_Z = var_Z ** 3.0
	else:
		var_Z = ( var_Z - 16.0 / 116.0 ) / 7.787

	ref_X =  95.047
	ref_Y = 100.000
	ref_Z = 108.883

	X = ref_X * var_X
	Y = ref_Y * var_Y
	Z = ref_Z * var_Z
	return (X, Y, Z)

def xyz_2_rgb(X, Y, Z):
	var_X = X / 100.0
	var_Y = Y / 100.0
	var_Z = Z / 100.0

	var_R = var_X *  3.2406 + var_Y * -1.5372 + var_Z * -0.4986
	var_G = var_X * -0.9689 + var_Y *  1.8758 + var_Z *  0.0415
	var_B = var_X *  0.0557 + var_Y * -0.2040 + var_Z *  1.0570

	if var_R > 0.0031308:
		var_R = 1.055 * ( var_R ** ( 1.0 / 2.4 ) ) - 0.055
	else:
		var_R = 12.92 * var_R
	if var_G > 0.0031308:
		var_G = 1.055 * ( var_G ** ( 1.0 / 2.4 ) ) - 0.055
	else:
		var_G = 12.92 * var_G
	if var_B > 0.0031308:
		var_B = 1.055 * ( var_B ** ( 1.0 / 2.4 ) ) - 0.055
	else:
		var_B = 12.92 * var_B

	R = var_R * 255
	G = var_G * 255
	B = var_B * 255
	return (R, G, B)

