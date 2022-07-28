import json
import os

class S2PConfigurator():
    def __init__(self, 
                #  config_dir,      # directory where the config is created
                 base_dir,      # Base dir where the configs and the output dirs for S2P execution will be placed
                #  ref_image_filename,
                #  ref_rpc_filename,
                #  sec_image_filename,
                #  sec_rpc_filename,
                 template_config_filename = None,  # template to use in the creation of the config
                 relative_paths_in_config = True,   # images and output dir in the config are relative to the config_filename
                 altitude_range = None,         # if min max altitudes are known, the disp range can be derived from these
                 tile_size = 600,
                 dsm_resolution = 0.3,
                 ):

        # self.config_dir = config_dir
        self.base_dir = base_dir
        # self.ref_image_filename = ref_image_filename
        # self.ref_rpc_filename = ref_rpc_filename
        # self.sec_image_filename = sec_image_filename
        # self.sec_rpc_filename = sec_rpc_filename
        self.template_config_filename = template_config_filename
        self.relative_paths_in_config = relative_paths_in_config
        self.altitude_range = altitude_range
        self.tile_size = tile_size
        self.dsm_resolution = dsm_resolution
        
        if template_config_filename is None:
            self.config = self.template_configuration()
        else:
            self.load_config(template_config_filename) 
        

        self.set_init_parameters()
    
        

    def set_filenames(self, ref_image_filename, ref_rpc_filename,
                            sec_image_filename, sec_rpc_filename,
                            explicit_config_filename=None,
                            explicit_output_dir=None):
        
        if not explicit_config_filename is None:
            config_directory = os.path.dirname(explicit_config_filename)
        else:
            config_directory = self.base_dir
        
        if not explicit_output_dir is None:
            output_dir = explicit_output_dir
        else:
            ref_image_basename = os.path.splitext(os.path.basename(ref_image_filename))[0][:-5] # [:-5] to remove trailing chars introduced by blender
            sec_image_basename = os.path.splitext(os.path.basename(sec_image_filename))[0][:-5] # [:-5] to remove trailing chars introduced by blender
            output_dir = os.path.join(config_directory, f'ref_{ref_image_basename}_sec_{sec_image_basename}')

        if self.relative_paths_in_config:
            self.config['out_dir'] = os.path.relpath(output_dir, config_directory)
            self.config['images'][0]['img'] = os.path.relpath(ref_image_filename, config_directory)
            self.config['images'][1]['img'] = os.path.relpath(sec_image_filename, config_directory)
            self.config['images'][0]['rpc'] = os.path.relpath(ref_rpc_filename, config_directory)
            self.config['images'][1]['rpc'] = os.path.relpath(sec_rpc_filename, config_directory)
        else:
            self.config['out_dir'] = output_dir
            self.config['images'][0]['img'] = ref_image_filename
            self.config['images'][1]['img'] = sec_image_filename
            self.config['images'][0]['rpc'] = ref_rpc_filename
            self.config['images'][1]['rpc'] = sec_rpc_filename


    def set_altitude_range(self):
        if not self.altitude_range is None:
            self.config["alt_min"] = self.altitude_range[0]
            self.config["alt_max"] = self.altitude_range[1]
            self.config["disp_range_method"] =  "fixed_altitude_range"

    def set_init_parameters(self):
        self.set_altitude_range()
        self.config["dsm_resolution"] = self.dsm_resolution
        self.config["tile_size"] = self.tile_size

    def set_parameter(self, param_name, param_value):       
        self.config[param_name] = param_value


    def save_config(self, s2p_config_filename):
        with open(s2p_config_filename,'w') as f:
            json.dump(self.config, f, indent=2)
            
    def load_config(self, s2p_config_filename):
        with open(s2p_config_filename, 'r') as fp:
            self.config = json.load(fp)
    
    

    def create_config(self, ref_image_filename, ref_rpc_filename,
                            sec_image_filename, sec_rpc_filename,
                            explicit_config_filename=None,
                            explicit_output_dir=None,
                            overwrite=False):
        
        # set the files in the config dictionary
        self.set_filenames(ref_image_filename, ref_rpc_filename,
                            sec_image_filename, sec_rpc_filename,
                            explicit_config_filename,
                            explicit_output_dir)
        
        # if no explicit filename for the config generate a filename based on the image names
        if not explicit_config_filename is None:
            config_filename = explicit_config_filename
        else:
            ref_image_basename = os.path.splitext(os.path.basename(ref_image_filename))[0][:-5] # [:-5] to remove trailing chars introduced by blender
            sec_image_basename = os.path.splitext(os.path.basename(sec_image_filename))[0][:-5] # [:-5] to remove trailing chars introduced by blender
            config_filename = os.path.join(self.base_dir, f's2p_config_ref_{ref_image_basename}_sec_{sec_image_basename}.json')
        
        if not os.path.isfile(config_filename) or overwrite:
            # create directory if necessary
            os.makedirs(os.path.dirname(config_filename), exist_ok=True)
            # save config            
            self.save_config(config_filename)

        return(config_filename)


    @staticmethod
    def template_configuration():
        template =  {"out_dir": "ref_ze_000.0_ref_az_000.0_sec_ze_005.0_sec_az_000.0",
                "images": [
                    {
                    "clr": None,
                    "img": "../../IMAGES/ze_000.0_az_000.0_0001.tif",
                    "rpc": "../../RPCFIT/rpcfit_ze_000.0_az_000.0.txt",
                    "wat": None,
                    "roi": None,
                    "cld": None
                    },
                    {
                    "img": "../../IMAGES/ze_005.0_az_000.0_0001.tif",
                    "rpc": "../../RPCFIT/rpcfit_ze_005.0_az_000.0.txt"
                    }
                ],
                "utm_zone": "21S",
                "utm_bbx": [
                    354062.8000007331,
                    354269.44000894425,
                    6182283.650013351,
                    6182474.090020918
                ],
                "ll_bbx": [
                    -58.58942456706418,
                    -58.58714224838392,
                    -34.490735394129494,
                    -34.48904787864305
                ],
                "roi": {
                    "y": 20014,
                    "x": 15798,
                    "w": 1899,
                    "h": 1975
                },
                "full_img": True,
                "tile_size": 600,
                "dsm_resolution": 0.3,
                "dsm_radius": 1,
                "msk_erosion": 0,
                "debug": False,
                "clean_intermediate": False,
                "matching_algorithm": "mgm_multi",
                "rpc_alt_range_scale_factor": 1,
                "triangulation_mode": "pairwise",
                "max_pointing_error": 10,
                "vertical_margin": 5,
                "skip_existing": False,
                "use_global_pointing_for_geometric_triangulation": False,
                "n_gcp_per_axis": 5,
                "max_processes": None,
                "temporary_dir": "/tmp",
                "horizontal_margin": 20,
                "cargarse_basura": True,
                "disp_max": None,
                "stereo_regularity_multiplier": 1.0,
                "disp_range_exogenous_high_margin": 100,
                "fusion_thresh": 3,
                "disp_range_srtm_high_margin": 50,
                "clean_tmp": True,
                "alt_min": -5,
                "register_with_shear": True,
                "alt_max": 35,
                "sift_match_thresh": 0.6,
                "exogenous_dem_geoid_mode": True,
                "stereo_speckle_filter": 25,
                "disp_min": None,
                "disp_range_exogenous_low_margin": -10,
                "disp_range_srtm_low_margin": -20,
                "disable_srtm": True,
                "fusion_operator": "average_if_close",
                "dsm_sigma": None,
                "census_ncc_win": 5,
                "omp_num_threads": 1,
                "disp_range_extra_margin": 0.2,
                "subsampling_factor": 1,
                "relative_sift_match_thresh": True,
                "epipolar_thresh": 0.5,
                "exogenous_dem": None,
                "disp_range_method": "fixed_altitude_range",
                }
        return template

if __name__ == "__main__":
    template_config_filename = '/media/agomez/SeagateGoFlex750GB/SATELITE/DATA_BLENDER/SIMULACIONES/CYLINDER_TEST_SIMSATOOL/S2P_CONFIG/s2p_config_template.json'
    s2p_config = S2PConfigurator('aca_config','aca_output_dir',
                                ',ref','ref_rpc','sec', 'sec_rpc',
                                 template_config_filename,
                                 relative_paths_in_config = True,
                                 altitude_range=[-2,2])
    
    print(s2p_config.config)



