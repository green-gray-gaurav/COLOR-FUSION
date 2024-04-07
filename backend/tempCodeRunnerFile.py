f (request.method == 'POST'):
        data = request.get_json()
        print(data)

        base_image = PIL.Image.open(urllib.request.urlopen(data['image1']))
        input_image = PIL.Image.open(urllib.request.urlopen(data['image2']))
        alpha = float(data['alpha'])
        clusters = int(data['clusters'])
        beta = float(data['beta'])
        enchant = data['enchant']
        shift = data['shift']
        version = data['version']

        base_image.save("backend/assets/base_image." + base_image.format)
        input_image.save("backend/assets/input_image." + input_image.format)

        if (version == 'version1'):
            fusion_kMeans(np.array(base