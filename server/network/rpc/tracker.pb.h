// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tracker.proto

#ifndef PROTOBUF_tracker_2eproto__INCLUDED
#define PROTOBUF_tracker_2eproto__INCLUDED

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 2006000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 2006001 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/service.h>
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)

namespace tracker {

// Internal implementation detail -- do not call these.
void  protobuf_AddDesc_tracker_2eproto();
void protobuf_AssignDesc_tracker_2eproto();
void protobuf_ShutdownFile_tracker_2eproto();

class F2TRegisterRequest;
class F2TRegisterResponse;
class F2TAddrRequest;
class F2TAddrResponse;
class F2TUpdateStreamRequest;
class F2TUpdateStreamResponse;

// ===================================================================

class F2TRegisterRequest : public ::google::protobuf::Message {
 public:
  F2TRegisterRequest();
  virtual ~F2TRegisterRequest();

  F2TRegisterRequest(const F2TRegisterRequest& from);

  inline F2TRegisterRequest& operator=(const F2TRegisterRequest& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const F2TRegisterRequest& default_instance();

  void Swap(F2TRegisterRequest* other);

  // implements Message ----------------------------------------------

  F2TRegisterRequest* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const F2TRegisterRequest& from);
  void MergeFrom(const F2TRegisterRequest& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required uint32 ip = 1;
  inline bool has_ip() const;
  inline void clear_ip();
  static const int kIpFieldNumber = 1;
  inline ::google::protobuf::uint32 ip() const;
  inline void set_ip(::google::protobuf::uint32 value);

  // required uint32 port = 2;
  inline bool has_port() const;
  inline void clear_port();
  static const int kPortFieldNumber = 2;
  inline ::google::protobuf::uint32 port() const;
  inline void set_port(::google::protobuf::uint32 value);

  // required uint32 asn = 3;
  inline bool has_asn() const;
  inline void clear_asn();
  static const int kAsnFieldNumber = 3;
  inline ::google::protobuf::uint32 asn() const;
  inline void set_asn(::google::protobuf::uint32 value);

  // required uint32 region = 4;
  inline bool has_region() const;
  inline void clear_region();
  static const int kRegionFieldNumber = 4;
  inline ::google::protobuf::uint32 region() const;
  inline void set_region(::google::protobuf::uint32 value);

  // @@protoc_insertion_point(class_scope:tracker.F2TRegisterRequest)
 private:
  inline void set_has_ip();
  inline void clear_has_ip();
  inline void set_has_port();
  inline void clear_has_port();
  inline void set_has_asn();
  inline void clear_has_asn();
  inline void set_has_region();
  inline void clear_has_region();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::uint32 ip_;
  ::google::protobuf::uint32 port_;
  ::google::protobuf::uint32 asn_;
  ::google::protobuf::uint32 region_;
  friend void  protobuf_AddDesc_tracker_2eproto();
  friend void protobuf_AssignDesc_tracker_2eproto();
  friend void protobuf_ShutdownFile_tracker_2eproto();

  void InitAsDefaultInstance();
  static F2TRegisterRequest* default_instance_;
};
// -------------------------------------------------------------------

class F2TRegisterResponse : public ::google::protobuf::Message {
 public:
  F2TRegisterResponse();
  virtual ~F2TRegisterResponse();

  F2TRegisterResponse(const F2TRegisterResponse& from);

  inline F2TRegisterResponse& operator=(const F2TRegisterResponse& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const F2TRegisterResponse& default_instance();

  void Swap(F2TRegisterResponse* other);

  // implements Message ----------------------------------------------

  F2TRegisterResponse* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const F2TRegisterResponse& from);
  void MergeFrom(const F2TRegisterResponse& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required uint32 result = 1;
  inline bool has_result() const;
  inline void clear_result();
  static const int kResultFieldNumber = 1;
  inline ::google::protobuf::uint32 result() const;
  inline void set_result(::google::protobuf::uint32 value);

  // @@protoc_insertion_point(class_scope:tracker.F2TRegisterResponse)
 private:
  inline void set_has_result();
  inline void clear_has_result();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::uint32 result_;
  friend void  protobuf_AddDesc_tracker_2eproto();
  friend void protobuf_AssignDesc_tracker_2eproto();
  friend void protobuf_ShutdownFile_tracker_2eproto();

  void InitAsDefaultInstance();
  static F2TRegisterResponse* default_instance_;
};
// -------------------------------------------------------------------

class F2TAddrRequest : public ::google::protobuf::Message {
 public:
  F2TAddrRequest();
  virtual ~F2TAddrRequest();

  F2TAddrRequest(const F2TAddrRequest& from);

  inline F2TAddrRequest& operator=(const F2TAddrRequest& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const F2TAddrRequest& default_instance();

  void Swap(F2TAddrRequest* other);

  // implements Message ----------------------------------------------

  F2TAddrRequest* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const F2TAddrRequest& from);
  void MergeFrom(const F2TAddrRequest& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required uint32 ip = 1;
  inline bool has_ip() const;
  inline void clear_ip();
  static const int kIpFieldNumber = 1;
  inline ::google::protobuf::uint32 ip() const;
  inline void set_ip(::google::protobuf::uint32 value);

  // required uint32 port = 2;
  inline bool has_port() const;
  inline void clear_port();
  static const int kPortFieldNumber = 2;
  inline ::google::protobuf::uint32 port() const;
  inline void set_port(::google::protobuf::uint32 value);

  // required uint32 asn = 3;
  inline bool has_asn() const;
  inline void clear_asn();
  static const int kAsnFieldNumber = 3;
  inline ::google::protobuf::uint32 asn() const;
  inline void set_asn(::google::protobuf::uint32 value);

  // required uint32 region = 4;
  inline bool has_region() const;
  inline void clear_region();
  static const int kRegionFieldNumber = 4;
  inline ::google::protobuf::uint32 region() const;
  inline void set_region(::google::protobuf::uint32 value);

  // required uint32 level = 5;
  inline bool has_level() const;
  inline void clear_level();
  static const int kLevelFieldNumber = 5;
  inline ::google::protobuf::uint32 level() const;
  inline void set_level(::google::protobuf::uint32 value);

  // @@protoc_insertion_point(class_scope:tracker.F2TAddrRequest)
 private:
  inline void set_has_ip();
  inline void clear_has_ip();
  inline void set_has_port();
  inline void clear_has_port();
  inline void set_has_asn();
  inline void clear_has_asn();
  inline void set_has_region();
  inline void clear_has_region();
  inline void set_has_level();
  inline void clear_has_level();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::uint32 ip_;
  ::google::protobuf::uint32 port_;
  ::google::protobuf::uint32 asn_;
  ::google::protobuf::uint32 region_;
  ::google::protobuf::uint32 level_;
  friend void  protobuf_AddDesc_tracker_2eproto();
  friend void protobuf_AssignDesc_tracker_2eproto();
  friend void protobuf_ShutdownFile_tracker_2eproto();

  void InitAsDefaultInstance();
  static F2TAddrRequest* default_instance_;
};
// -------------------------------------------------------------------

class F2TAddrResponse : public ::google::protobuf::Message {
 public:
  F2TAddrResponse();
  virtual ~F2TAddrResponse();

  F2TAddrResponse(const F2TAddrResponse& from);

  inline F2TAddrResponse& operator=(const F2TAddrResponse& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const F2TAddrResponse& default_instance();

  void Swap(F2TAddrResponse* other);

  // implements Message ----------------------------------------------

  F2TAddrResponse* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const F2TAddrResponse& from);
  void MergeFrom(const F2TAddrResponse& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required uint32 ip = 1;
  inline bool has_ip() const;
  inline void clear_ip();
  static const int kIpFieldNumber = 1;
  inline ::google::protobuf::uint32 ip() const;
  inline void set_ip(::google::protobuf::uint32 value);

  // required uint32 port = 2;
  inline bool has_port() const;
  inline void clear_port();
  static const int kPortFieldNumber = 2;
  inline ::google::protobuf::uint32 port() const;
  inline void set_port(::google::protobuf::uint32 value);

  // required uint32 result = 3;
  inline bool has_result() const;
  inline void clear_result();
  static const int kResultFieldNumber = 3;
  inline ::google::protobuf::uint32 result() const;
  inline void set_result(::google::protobuf::uint32 value);

  // required uint32 level = 4;
  inline bool has_level() const;
  inline void clear_level();
  static const int kLevelFieldNumber = 4;
  inline ::google::protobuf::uint32 level() const;
  inline void set_level(::google::protobuf::uint32 value);

  // @@protoc_insertion_point(class_scope:tracker.F2TAddrResponse)
 private:
  inline void set_has_ip();
  inline void clear_has_ip();
  inline void set_has_port();
  inline void clear_has_port();
  inline void set_has_result();
  inline void clear_has_result();
  inline void set_has_level();
  inline void clear_has_level();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::uint32 ip_;
  ::google::protobuf::uint32 port_;
  ::google::protobuf::uint32 result_;
  ::google::protobuf::uint32 level_;
  friend void  protobuf_AddDesc_tracker_2eproto();
  friend void protobuf_AssignDesc_tracker_2eproto();
  friend void protobuf_ShutdownFile_tracker_2eproto();

  void InitAsDefaultInstance();
  static F2TAddrResponse* default_instance_;
};
// -------------------------------------------------------------------

class F2TUpdateStreamRequest : public ::google::protobuf::Message {
 public:
  F2TUpdateStreamRequest();
  virtual ~F2TUpdateStreamRequest();

  F2TUpdateStreamRequest(const F2TUpdateStreamRequest& from);

  inline F2TUpdateStreamRequest& operator=(const F2TUpdateStreamRequest& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const F2TUpdateStreamRequest& default_instance();

  void Swap(F2TUpdateStreamRequest* other);

  // implements Message ----------------------------------------------

  F2TUpdateStreamRequest* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const F2TUpdateStreamRequest& from);
  void MergeFrom(const F2TUpdateStreamRequest& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required uint32 cmd = 1;
  inline bool has_cmd() const;
  inline void clear_cmd();
  static const int kCmdFieldNumber = 1;
  inline ::google::protobuf::uint32 cmd() const;
  inline void set_cmd(::google::protobuf::uint32 value);

  // required uint32 level = 2;
  inline bool has_level() const;
  inline void clear_level();
  static const int kLevelFieldNumber = 2;
  inline ::google::protobuf::uint32 level() const;
  inline void set_level(::google::protobuf::uint32 value);

  // @@protoc_insertion_point(class_scope:tracker.F2TUpdateStreamRequest)
 private:
  inline void set_has_cmd();
  inline void clear_has_cmd();
  inline void set_has_level();
  inline void clear_has_level();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::uint32 cmd_;
  ::google::protobuf::uint32 level_;
  friend void  protobuf_AddDesc_tracker_2eproto();
  friend void protobuf_AssignDesc_tracker_2eproto();
  friend void protobuf_ShutdownFile_tracker_2eproto();

  void InitAsDefaultInstance();
  static F2TUpdateStreamRequest* default_instance_;
};
// -------------------------------------------------------------------

class F2TUpdateStreamResponse : public ::google::protobuf::Message {
 public:
  F2TUpdateStreamResponse();
  virtual ~F2TUpdateStreamResponse();

  F2TUpdateStreamResponse(const F2TUpdateStreamResponse& from);

  inline F2TUpdateStreamResponse& operator=(const F2TUpdateStreamResponse& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const F2TUpdateStreamResponse& default_instance();

  void Swap(F2TUpdateStreamResponse* other);

  // implements Message ----------------------------------------------

  F2TUpdateStreamResponse* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const F2TUpdateStreamResponse& from);
  void MergeFrom(const F2TUpdateStreamResponse& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required uint32 result = 1;
  inline bool has_result() const;
  inline void clear_result();
  static const int kResultFieldNumber = 1;
  inline ::google::protobuf::uint32 result() const;
  inline void set_result(::google::protobuf::uint32 value);

  // @@protoc_insertion_point(class_scope:tracker.F2TUpdateStreamResponse)
 private:
  inline void set_has_result();
  inline void clear_has_result();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::uint32 result_;
  friend void  protobuf_AddDesc_tracker_2eproto();
  friend void protobuf_AssignDesc_tracker_2eproto();
  friend void protobuf_ShutdownFile_tracker_2eproto();

  void InitAsDefaultInstance();
  static F2TUpdateStreamResponse* default_instance_;
};
// ===================================================================

class EchoService_Stub;

class EchoService : public ::google::protobuf::Service {
 protected:
  // This class should be treated as an abstract interface.
  inline EchoService() {};
 public:
  virtual ~EchoService();

  typedef EchoService_Stub Stub;

  static const ::google::protobuf::ServiceDescriptor* descriptor();

  virtual void Register(::google::protobuf::RpcController* controller,
                       const ::tracker::F2TRegisterRequest* request,
                       ::tracker::F2TRegisterResponse* response,
                       ::google::protobuf::Closure* done);
  virtual void GetAddr(::google::protobuf::RpcController* controller,
                       const ::tracker::F2TAddrRequest* request,
                       ::tracker::F2TAddrResponse* response,
                       ::google::protobuf::Closure* done);
  virtual void UpdateStream(::google::protobuf::RpcController* controller,
                       const ::tracker::F2TUpdateStreamRequest* request,
                       ::tracker::F2TUpdateStreamResponse* response,
                       ::google::protobuf::Closure* done);

  // implements Service ----------------------------------------------

  const ::google::protobuf::ServiceDescriptor* GetDescriptor();
  void CallMethod(const ::google::protobuf::MethodDescriptor* method,
                  ::google::protobuf::RpcController* controller,
                  const ::google::protobuf::Message* request,
                  ::google::protobuf::Message* response,
                  ::google::protobuf::Closure* done);
  const ::google::protobuf::Message& GetRequestPrototype(
    const ::google::protobuf::MethodDescriptor* method) const;
  const ::google::protobuf::Message& GetResponsePrototype(
    const ::google::protobuf::MethodDescriptor* method) const;

 private:
  GOOGLE_DISALLOW_EVIL_CONSTRUCTORS(EchoService);
};

class EchoService_Stub : public EchoService {
 public:
  EchoService_Stub(::google::protobuf::RpcChannel* channel);
  EchoService_Stub(::google::protobuf::RpcChannel* channel,
                   ::google::protobuf::Service::ChannelOwnership ownership);
  ~EchoService_Stub();

  inline ::google::protobuf::RpcChannel* channel() { return channel_; }

  // implements EchoService ------------------------------------------

  void Register(::google::protobuf::RpcController* controller,
                       const ::tracker::F2TRegisterRequest* request,
                       ::tracker::F2TRegisterResponse* response,
                       ::google::protobuf::Closure* done);
  void GetAddr(::google::protobuf::RpcController* controller,
                       const ::tracker::F2TAddrRequest* request,
                       ::tracker::F2TAddrResponse* response,
                       ::google::protobuf::Closure* done);
  void UpdateStream(::google::protobuf::RpcController* controller,
                       const ::tracker::F2TUpdateStreamRequest* request,
                       ::tracker::F2TUpdateStreamResponse* response,
                       ::google::protobuf::Closure* done);
 private:
  ::google::protobuf::RpcChannel* channel_;
  bool owns_channel_;
  GOOGLE_DISALLOW_EVIL_CONSTRUCTORS(EchoService_Stub);
};


// ===================================================================


// ===================================================================

// F2TRegisterRequest

// required uint32 ip = 1;
inline bool F2TRegisterRequest::has_ip() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void F2TRegisterRequest::set_has_ip() {
  _has_bits_[0] |= 0x00000001u;
}
inline void F2TRegisterRequest::clear_has_ip() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void F2TRegisterRequest::clear_ip() {
  ip_ = 0u;
  clear_has_ip();
}
inline ::google::protobuf::uint32 F2TRegisterRequest::ip() const {
  // @@protoc_insertion_point(field_get:tracker.F2TRegisterRequest.ip)
  return ip_;
}
inline void F2TRegisterRequest::set_ip(::google::protobuf::uint32 value) {
  set_has_ip();
  ip_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TRegisterRequest.ip)
}

// required uint32 port = 2;
inline bool F2TRegisterRequest::has_port() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void F2TRegisterRequest::set_has_port() {
  _has_bits_[0] |= 0x00000002u;
}
inline void F2TRegisterRequest::clear_has_port() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void F2TRegisterRequest::clear_port() {
  port_ = 0u;
  clear_has_port();
}
inline ::google::protobuf::uint32 F2TRegisterRequest::port() const {
  // @@protoc_insertion_point(field_get:tracker.F2TRegisterRequest.port)
  return port_;
}
inline void F2TRegisterRequest::set_port(::google::protobuf::uint32 value) {
  set_has_port();
  port_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TRegisterRequest.port)
}

// required uint32 asn = 3;
inline bool F2TRegisterRequest::has_asn() const {
  return (_has_bits_[0] & 0x00000004u) != 0;
}
inline void F2TRegisterRequest::set_has_asn() {
  _has_bits_[0] |= 0x00000004u;
}
inline void F2TRegisterRequest::clear_has_asn() {
  _has_bits_[0] &= ~0x00000004u;
}
inline void F2TRegisterRequest::clear_asn() {
  asn_ = 0u;
  clear_has_asn();
}
inline ::google::protobuf::uint32 F2TRegisterRequest::asn() const {
  // @@protoc_insertion_point(field_get:tracker.F2TRegisterRequest.asn)
  return asn_;
}
inline void F2TRegisterRequest::set_asn(::google::protobuf::uint32 value) {
  set_has_asn();
  asn_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TRegisterRequest.asn)
}

// required uint32 region = 4;
inline bool F2TRegisterRequest::has_region() const {
  return (_has_bits_[0] & 0x00000008u) != 0;
}
inline void F2TRegisterRequest::set_has_region() {
  _has_bits_[0] |= 0x00000008u;
}
inline void F2TRegisterRequest::clear_has_region() {
  _has_bits_[0] &= ~0x00000008u;
}
inline void F2TRegisterRequest::clear_region() {
  region_ = 0u;
  clear_has_region();
}
inline ::google::protobuf::uint32 F2TRegisterRequest::region() const {
  // @@protoc_insertion_point(field_get:tracker.F2TRegisterRequest.region)
  return region_;
}
inline void F2TRegisterRequest::set_region(::google::protobuf::uint32 value) {
  set_has_region();
  region_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TRegisterRequest.region)
}

// -------------------------------------------------------------------

// F2TRegisterResponse

// required uint32 result = 1;
inline bool F2TRegisterResponse::has_result() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void F2TRegisterResponse::set_has_result() {
  _has_bits_[0] |= 0x00000001u;
}
inline void F2TRegisterResponse::clear_has_result() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void F2TRegisterResponse::clear_result() {
  result_ = 0u;
  clear_has_result();
}
inline ::google::protobuf::uint32 F2TRegisterResponse::result() const {
  // @@protoc_insertion_point(field_get:tracker.F2TRegisterResponse.result)
  return result_;
}
inline void F2TRegisterResponse::set_result(::google::protobuf::uint32 value) {
  set_has_result();
  result_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TRegisterResponse.result)
}

// -------------------------------------------------------------------

// F2TAddrRequest

// required uint32 ip = 1;
inline bool F2TAddrRequest::has_ip() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void F2TAddrRequest::set_has_ip() {
  _has_bits_[0] |= 0x00000001u;
}
inline void F2TAddrRequest::clear_has_ip() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void F2TAddrRequest::clear_ip() {
  ip_ = 0u;
  clear_has_ip();
}
inline ::google::protobuf::uint32 F2TAddrRequest::ip() const {
  // @@protoc_insertion_point(field_get:tracker.F2TAddrRequest.ip)
  return ip_;
}
inline void F2TAddrRequest::set_ip(::google::protobuf::uint32 value) {
  set_has_ip();
  ip_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TAddrRequest.ip)
}

// required uint32 port = 2;
inline bool F2TAddrRequest::has_port() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void F2TAddrRequest::set_has_port() {
  _has_bits_[0] |= 0x00000002u;
}
inline void F2TAddrRequest::clear_has_port() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void F2TAddrRequest::clear_port() {
  port_ = 0u;
  clear_has_port();
}
inline ::google::protobuf::uint32 F2TAddrRequest::port() const {
  // @@protoc_insertion_point(field_get:tracker.F2TAddrRequest.port)
  return port_;
}
inline void F2TAddrRequest::set_port(::google::protobuf::uint32 value) {
  set_has_port();
  port_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TAddrRequest.port)
}

// required uint32 asn = 3;
inline bool F2TAddrRequest::has_asn() const {
  return (_has_bits_[0] & 0x00000004u) != 0;
}
inline void F2TAddrRequest::set_has_asn() {
  _has_bits_[0] |= 0x00000004u;
}
inline void F2TAddrRequest::clear_has_asn() {
  _has_bits_[0] &= ~0x00000004u;
}
inline void F2TAddrRequest::clear_asn() {
  asn_ = 0u;
  clear_has_asn();
}
inline ::google::protobuf::uint32 F2TAddrRequest::asn() const {
  // @@protoc_insertion_point(field_get:tracker.F2TAddrRequest.asn)
  return asn_;
}
inline void F2TAddrRequest::set_asn(::google::protobuf::uint32 value) {
  set_has_asn();
  asn_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TAddrRequest.asn)
}

// required uint32 region = 4;
inline bool F2TAddrRequest::has_region() const {
  return (_has_bits_[0] & 0x00000008u) != 0;
}
inline void F2TAddrRequest::set_has_region() {
  _has_bits_[0] |= 0x00000008u;
}
inline void F2TAddrRequest::clear_has_region() {
  _has_bits_[0] &= ~0x00000008u;
}
inline void F2TAddrRequest::clear_region() {
  region_ = 0u;
  clear_has_region();
}
inline ::google::protobuf::uint32 F2TAddrRequest::region() const {
  // @@protoc_insertion_point(field_get:tracker.F2TAddrRequest.region)
  return region_;
}
inline void F2TAddrRequest::set_region(::google::protobuf::uint32 value) {
  set_has_region();
  region_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TAddrRequest.region)
}

// required uint32 level = 5;
inline bool F2TAddrRequest::has_level() const {
  return (_has_bits_[0] & 0x00000010u) != 0;
}
inline void F2TAddrRequest::set_has_level() {
  _has_bits_[0] |= 0x00000010u;
}
inline void F2TAddrRequest::clear_has_level() {
  _has_bits_[0] &= ~0x00000010u;
}
inline void F2TAddrRequest::clear_level() {
  level_ = 0u;
  clear_has_level();
}
inline ::google::protobuf::uint32 F2TAddrRequest::level() const {
  // @@protoc_insertion_point(field_get:tracker.F2TAddrRequest.level)
  return level_;
}
inline void F2TAddrRequest::set_level(::google::protobuf::uint32 value) {
  set_has_level();
  level_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TAddrRequest.level)
}

// -------------------------------------------------------------------

// F2TAddrResponse

// required uint32 ip = 1;
inline bool F2TAddrResponse::has_ip() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void F2TAddrResponse::set_has_ip() {
  _has_bits_[0] |= 0x00000001u;
}
inline void F2TAddrResponse::clear_has_ip() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void F2TAddrResponse::clear_ip() {
  ip_ = 0u;
  clear_has_ip();
}
inline ::google::protobuf::uint32 F2TAddrResponse::ip() const {
  // @@protoc_insertion_point(field_get:tracker.F2TAddrResponse.ip)
  return ip_;
}
inline void F2TAddrResponse::set_ip(::google::protobuf::uint32 value) {
  set_has_ip();
  ip_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TAddrResponse.ip)
}

// required uint32 port = 2;
inline bool F2TAddrResponse::has_port() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void F2TAddrResponse::set_has_port() {
  _has_bits_[0] |= 0x00000002u;
}
inline void F2TAddrResponse::clear_has_port() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void F2TAddrResponse::clear_port() {
  port_ = 0u;
  clear_has_port();
}
inline ::google::protobuf::uint32 F2TAddrResponse::port() const {
  // @@protoc_insertion_point(field_get:tracker.F2TAddrResponse.port)
  return port_;
}
inline void F2TAddrResponse::set_port(::google::protobuf::uint32 value) {
  set_has_port();
  port_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TAddrResponse.port)
}

// required uint32 result = 3;
inline bool F2TAddrResponse::has_result() const {
  return (_has_bits_[0] & 0x00000004u) != 0;
}
inline void F2TAddrResponse::set_has_result() {
  _has_bits_[0] |= 0x00000004u;
}
inline void F2TAddrResponse::clear_has_result() {
  _has_bits_[0] &= ~0x00000004u;
}
inline void F2TAddrResponse::clear_result() {
  result_ = 0u;
  clear_has_result();
}
inline ::google::protobuf::uint32 F2TAddrResponse::result() const {
  // @@protoc_insertion_point(field_get:tracker.F2TAddrResponse.result)
  return result_;
}
inline void F2TAddrResponse::set_result(::google::protobuf::uint32 value) {
  set_has_result();
  result_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TAddrResponse.result)
}

// required uint32 level = 4;
inline bool F2TAddrResponse::has_level() const {
  return (_has_bits_[0] & 0x00000008u) != 0;
}
inline void F2TAddrResponse::set_has_level() {
  _has_bits_[0] |= 0x00000008u;
}
inline void F2TAddrResponse::clear_has_level() {
  _has_bits_[0] &= ~0x00000008u;
}
inline void F2TAddrResponse::clear_level() {
  level_ = 0u;
  clear_has_level();
}
inline ::google::protobuf::uint32 F2TAddrResponse::level() const {
  // @@protoc_insertion_point(field_get:tracker.F2TAddrResponse.level)
  return level_;
}
inline void F2TAddrResponse::set_level(::google::protobuf::uint32 value) {
  set_has_level();
  level_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TAddrResponse.level)
}

// -------------------------------------------------------------------

// F2TUpdateStreamRequest

// required uint32 cmd = 1;
inline bool F2TUpdateStreamRequest::has_cmd() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void F2TUpdateStreamRequest::set_has_cmd() {
  _has_bits_[0] |= 0x00000001u;
}
inline void F2TUpdateStreamRequest::clear_has_cmd() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void F2TUpdateStreamRequest::clear_cmd() {
  cmd_ = 0u;
  clear_has_cmd();
}
inline ::google::protobuf::uint32 F2TUpdateStreamRequest::cmd() const {
  // @@protoc_insertion_point(field_get:tracker.F2TUpdateStreamRequest.cmd)
  return cmd_;
}
inline void F2TUpdateStreamRequest::set_cmd(::google::protobuf::uint32 value) {
  set_has_cmd();
  cmd_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TUpdateStreamRequest.cmd)
}

// required uint32 level = 2;
inline bool F2TUpdateStreamRequest::has_level() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void F2TUpdateStreamRequest::set_has_level() {
  _has_bits_[0] |= 0x00000002u;
}
inline void F2TUpdateStreamRequest::clear_has_level() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void F2TUpdateStreamRequest::clear_level() {
  level_ = 0u;
  clear_has_level();
}
inline ::google::protobuf::uint32 F2TUpdateStreamRequest::level() const {
  // @@protoc_insertion_point(field_get:tracker.F2TUpdateStreamRequest.level)
  return level_;
}
inline void F2TUpdateStreamRequest::set_level(::google::protobuf::uint32 value) {
  set_has_level();
  level_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TUpdateStreamRequest.level)
}

// -------------------------------------------------------------------

// F2TUpdateStreamResponse

// required uint32 result = 1;
inline bool F2TUpdateStreamResponse::has_result() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void F2TUpdateStreamResponse::set_has_result() {
  _has_bits_[0] |= 0x00000001u;
}
inline void F2TUpdateStreamResponse::clear_has_result() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void F2TUpdateStreamResponse::clear_result() {
  result_ = 0u;
  clear_has_result();
}
inline ::google::protobuf::uint32 F2TUpdateStreamResponse::result() const {
  // @@protoc_insertion_point(field_get:tracker.F2TUpdateStreamResponse.result)
  return result_;
}
inline void F2TUpdateStreamResponse::set_result(::google::protobuf::uint32 value) {
  set_has_result();
  result_ = value;
  // @@protoc_insertion_point(field_set:tracker.F2TUpdateStreamResponse.result)
}


// @@protoc_insertion_point(namespace_scope)

}  // namespace tracker

#ifndef SWIG
namespace google {
namespace protobuf {


}  // namespace google
}  // namespace protobuf
#endif  // SWIG

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_tracker_2eproto__INCLUDED
