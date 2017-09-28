/**
* @file cache_manager.h
* @brief	This file define some classes for stream cache manager. \n
*			The most important class is class CacheManager, \n
*			it has two derive classes, UploaderCacheManager and BackendCacheManager, \n
*			using for module uploader and module backend. \n
*			CacheManager is an singleton in one process, it will manage the cache for many streams.  \n
*			For every stream, it has two cache stores, \n
*			LatestFragmentCache and HistoryFragmentCache, \n
*			using for cache live stream and timeshift stream. \n
*			Stream data was stored in cache as FLVFragment, about 10 second data, \n
* @author songshenyi
* <pre><b>copyright: Youku</b></pre>
* <pre><b>email: </b>songshenyi@youku.com</pre>
* <pre><b>company: </b>http://www.youku.com</pre>
* <pre><b>All rights reserved.</b></pre>
* @date 2014/05/29
* @see  fragment.h
*/

#pragma once

#include <assert.h>
#include <common/type_defs.h>

#include <map>
#include <vector>
#include <set>
#include <deque>
#include <string>
#include <list>

#include "fragment/fragment.h"
#include "fragment/fragment_generator.h"
#include "cache_watcher.h"

#include "util/linked_hash_map.h"
#include "util/xml.h"
#include "util/city.h"
#include <event.h>
#include "cache_manager_config.h"
#include "circular_cache.h"

#include "media_manager_state.h"

#include "media_manager_rtp_interface.h"
#include "whitelist_manager.h"
#include "../network/base_http_server.h"

#define CACHE_REQUEST_VERSION_2 2

#define CACHE_RESPONSE_VERSION_2 2

namespace media_manager {
  static const uint32_t CacheMassageMaxLen = 128;
  static const uint32_t KeepStreamAfterClose = 2 * 3600 * 1000; // millisecond

  enum CacheReqStatus {
    CACHE_REQ_STREAM_CONFIG = 1,
    CACHE_REQ_STOP = 9,

    CACHE_REQ_LIVE_FLV_HEADER = 100,
    CACHE_REQ_SHIFT_FLV_HEADER = 110,

    CACHE_REQ_LIVE_FLV_LATEST_KEY_BLOCK = 200,
    CACHE_REQ_LIVE_FLV_BLOCK = 201,
    CACHE_REQ_SHIFT_FLV_BLOCK = 210,

    CACHE_REQ_LIVE_FLV_LATEST_KEY_FRAGMENT = 300,
    CACHE_REQ_LIVE_FLV_LATEST_N_FRAGMENT = 301,
    CACHE_REQ_LIVE_FLV_LATEST_FRAGMENT = 302,

    CACHE_REQ_LIVE_FLV_FRAGMENT_BY_SEQ = 310,
    CACHE_REQ_LIVE_FLV_FRAGMENT_BY_TS = 311,
    // CACHE_REQ_SHIFT_FLV_FRAGMENT = 320,

    CACHE_REQ_LIVE_TS_LATEST_SEGMENT = 400,
    CACHE_REQ_LIVE_TS_LATEST_N_SEGMENT = 401,

    CACHE_REQ_LIVE_TS_SEGMENT_BY_SEQ = 420,

    CACHE_REQ_LIVE_SDP = 500,
    CACHE_REQ_LIVE_RTP = 510,

    CACHE_REQ_LIVE_FLV_LATEST_MINIBLOCK = 600,
    CACHE_REQ_LIVE_FLV_MINIBLOCK = 601,
    CACHE_REQ_LIVE_FLV_MINIBLOCK_HEADER = 610,
  };

  enum RateType {
    RATE_AUDIO = 0,					// only audio
    RATE_KEY_VIDEO_AND_AUDIO = 1,	// key frame and audio
    RATE_P_VIDEO_AND_AUDIO = 2,		// key frame, p frame and audio
    RATE_COMPLETE = 3				// full video and audio
  };

  enum ModuleType {
    MODULE_TYPE_UPLOADER = 1,
    MODULE_TYPE_BACKEND = 2
  };

  enum StreamStoreState {
    STREAM_STORE_CONSTRUCT = 0,
    STREAM_STORE_INIT = 1,
    //        STREAM_STORE_HEADER = 2,
    STREAM_STORE_ACTIVE = 2,
    STREAM_STORE_STOP = 3,
    STREAM_STORE_DESTROY = 4
  };

  class StreamStore {
  public:
    StreamStore(const StreamId_Ext& stream_id_ext);

    int32_t init(uint8_t module_type, CacheManagerConfig* cache_manager_config, CacheManager* cache_manager);

    void set_push_active();
    void set_req_active();
    time_t& get_push_active_time();
    time_t& get_req_active_time();

    ~StreamStore();

  public:
    StreamId_Ext stream_id;

    StreamStoreState state;

    fragment::FLVMiniBlockGenerator* flv_miniblock_generator;
    FLVMiniBlockCircularCache* flv_miniblock_cache;
    RTPMediaCache* rtp_media_cache;

  protected:
    time_t				_last_push_time;
    time_t				_last_req_time;
  };

  class UploaderCacheManagerInterface {
  public:
    virtual int32_t init_stream(const StreamId_Ext& stream_id) = 0;
    virtual int32_t set_flv_header(StreamId_Ext stream_id, flv_header* input_flv_header, uint32_t flv_header_len) = 0;
    virtual int32_t set_flv_tag(StreamId_Ext stream_id, flv_tag* input_flv_tag, bool malloc_new_memory_flag = true) = 0;
    virtual int32_t stop_stream(StreamId_Ext stream_id) = 0;
    virtual int32_t destroy_stream(StreamId_Ext stream_id) = 0;
    virtual int32_t register_watcher(cache_watch_handler handler, uint8_t watch_type = CACHE_WATCHING_ALL, void* arg = NULL) = 0;
    virtual ~UploaderCacheManagerInterface(){}
  };

  class PlayerCacheManagerInterface {
  public:
    // stream method.
    virtual int32_t init_stream(const StreamId_Ext& stream_id) = 0;

    // miniblock method
    virtual flv_header* get_miniblock_flv_header(StreamId_Ext stream_id, uint32_t& header_len, int32_t& status_code, bool req_from_backend = true) = 0;
    virtual fragment::FLVHeader* get_miniblock_flv_header(StreamId_Ext stream_id, fragment::FLVHeader &header, int32_t& status_code) = 0;
    virtual fragment::FLVMiniBlock* get_latest_miniblock(StreamId_Ext stream_id, int32_t& status_code, bool req_from_backend = true) = 0;
    virtual fragment::FLVMiniBlock* get_miniblock_by_seq(StreamId_Ext stream_id, int32_t seq, int32_t& status_code, bool req_from_backend = true) = 0;

    // other method
    virtual int32_t register_watcher(cache_watch_handler handler, uint8_t watch_type = CACHE_WATCHING_ALL, void* arg = NULL) = 0;
    virtual ~PlayerCacheManagerInterface(){}
  };

  void cache_manager_state(char* query, char* param, json_object* rsp);

  void cache_manager_stream_state(char* query, char* param, json_object* rsp);

  typedef void (CacheManager::*HttpHandler_t)(char* query, char* param, json_object* rsp);

  /**
  * @class	CacheManager
  * @brief	This is base cache manager class, \n
  *			you can use this class to get header/block/fragment. \n
  *			If you want to set value, you can use the derived classes.
  * @see		FLVBlock \n
  *			FLVFragment \n
  *			UploaderCacheManagerInterface \n
  *			BackendCacheManagerInterface \n
  *			PlayerCacheManagerInterface
  */
  class CacheManager :
    public UploaderCacheManagerInterface,
    public PlayerCacheManagerInterface,
    public MediaManagerRTPInterface {
  public:
    CacheManager(uint8_t module_type, CacheManagerConfig* config = NULL);

    void set_event_base(event_base* base);
    void set_http_server(http::HTTPServer *server);

    virtual ~CacheManager();
    static void Destroy();

    static UploaderCacheManagerInterface* get_uploader_cache_instance();
    static PlayerCacheManagerInterface* get_player_cache_instance();
    static MediaManagerRTPInterface* get_rtp_cache_instance();
    static CacheManager* get_cache_manager();

    // UploaderCacheManagerInterface
    int32_t init_stream(const StreamId_Ext& stream_id);
    int32_t set_flv_header(StreamId_Ext stream_id, flv_header* input_flv_header, uint32_t flv_header_len);
    int32_t set_flv_tag(StreamId_Ext stream_id, flv_tag* input_flv_tag, bool malloc_new_memory_flag = true);
    int32_t register_watcher(cache_watch_handler handler, uint8_t watch_type, void* arg);
    int32_t destroy_stream();
    int32_t destroy_stream(StreamId_Ext stream_id);
    int32_t destroy_stream(uint32_t stream_id);

    // PlayerCacheManagerInterface

    // miniblock method
    flv_header* get_miniblock_flv_header(StreamId_Ext stream_id, uint32_t& header_len, int32_t& status_code, bool req_from_backend = true);
    fragment::FLVHeader* get_miniblock_flv_header(StreamId_Ext stream_id, fragment::FLVHeader &header, int32_t& status_code);
    fragment::FLVMiniBlock* get_latest_miniblock(StreamId_Ext stream_id, int32_t& status_code, bool req_from_backend = true);
    fragment::FLVMiniBlock* get_miniblock_by_seq(StreamId_Ext stream_id, int32_t seq, int32_t& status_code, bool req_from_backend = true);

    int32_t load_config(const CacheManagerConfig* config);

    void timer_service(const int32_t fd, short which, void *arg);
    void start_timer();
    void stop_timer();

    void http_state(char* query, char* param, json_object* rsp);

    // MediaManagerRTPInterface
    virtual RTPMediaCache* get_rtp_media_cache(const StreamId_Ext& stream_id, int32_t& status_code, bool req_from_backend = true);

    virtual int32_t notify_watcher(StreamId_Ext& stream_id, uint8_t watch_type);

    virtual void on_timer();

    StreamStore* get_stream_store(StreamId_Ext& stream_id, int32_t& status_code);

  protected:
    bool contains_stream(const StreamId_Ext& stream_id);
    int32_t _notify_watcher(StreamId_Ext& stream_id, uint8_t watch_type = CACHE_WATCHING_ALL);
    int32_t _req_from_backend(StreamId_Ext stream_id, int32_t request_state, int32_t seq = 0);
    int32_t _req_from_backend_rtp(StreamId_Ext stream_id, int32_t request_state);
    int32_t _req_stop_from_backend(StreamId_Ext stream_id, int32_t request_state, int32_t seq = 0);
    int32_t _req_stop_from_backend(uint32_t stream_id);
    int32_t _req_stop_from_backend_rtp(StreamId_Ext stream_id);
    int32_t _req_stop_from_backend(StreamId_Ext stream_id);

    void _check_stream_store_timeout();

    void _adjust_flv_miniblock_cache_size();

    int32_t _destroy_stream_store();
    int32_t _destroy_stream_store(StreamId_Ext& stream_id);
    int32_t _destroy_stream_store(uint32_t stream_id);

    // http state api
    void _init_http_server();
    void _add_http_handler(const char* query, const char* param, HttpHandler_t handler);
    void _state(char* query, char* param, json_object* rsp);
    void _stream_list(char* query, char* param, json_object* rsp);
    void _store_state(char* query, char* param, json_object* rsp);
    void _whitelist_fake(char* query, char* param, json_object* rsp);
    void _live_cache_state(CircularCache* cache, json_object* rsp);
    void _fragment_generator_state(fragment::FragmentGenerator* generator, json_object* rsp);
    void _flv_miniblock_generator_state(fragment::FLVMiniBlockGenerator* generator, json_object* rsp);
    void _flv_live_miniblock_cache_state(FLVMiniBlockCircularCache* cache, json_object* rsp);

  protected:
    typedef __gnu_cxx::hash_map<StreamId_Ext, StreamStore*> StreamStoreMap_t;
    StreamStoreMap_t _stream_store_map;

    typedef std::map<std::string, HttpHandler_t> HttpHandlerMap_t;
    HttpHandlerMap_t _http_handler_map;

    std::vector<CacheWatcher*> _notify_handle_vec;

    uint8_t		_module_type;

    static CacheManager* _instance;

    struct event _ev_timer;

    struct event_base* _main_base;

    bool _time_service_active;

    CacheManagerConfig*		_config;
  };

}
